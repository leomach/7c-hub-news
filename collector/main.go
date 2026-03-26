package main

import (
	"context"
	"flag"
	"log"
	"sync"
	"time"

	"7c-hub-news/collector/config"
	"7c-hub-news/collector/dedup"
	"7c-hub-news/collector/fetcher"
	"7c-hub-news/collector/model"
	"7c-hub-news/collector/output"
)

func main() {
	configPath := flag.String("config", "../sources.yaml", "path to sources.yaml")
	outputPath := flag.String("output", "../output/news.json", "path to output news.json")
	flag.Parse()

	cfg, err := config.LoadConfig(*configPath)
	if err != nil {
		log.Fatalf("Error loading config: %v", err)
	}

	ctx := context.Background()
	var wg sync.WaitGroup
	itemsChan := make(chan model.NewsItem, 500)
	errorsChan := make(chan model.CollectorError, 50)

	rssFetcher := fetcher.NewRSSFetcher()
	hnFetcher := fetcher.NewHNFetcher()
	tabNewsFetcher := fetcher.NewTabNewsFetcher()

	sourcesAttempted := 0
	for _, src := range cfg.Sources {
		if !src.Enabled {
			continue
		}
		sourcesAttempted++

		wg.Add(1)
		go func(src config.Source) {
			defer wg.Done()
			
			var f fetcher.Fetcher
			switch src.Type {
			case "rss":
				f = rssFetcher
			case "rest_hackernews":
				f = hnFetcher
			case "rest_tabnews":
				f = tabNewsFetcher
			default:
				log.Printf("Unknown source type: %s for source %s", src.Type, src.ID)
				return
			}

			fetchCtx, cancel := context.WithTimeout(ctx, time.Duration(cfg.Settings.FetchTimeoutSeconds)*time.Second)
			defer cancel()

			items, err := f.Fetch(fetchCtx, src)
			if err != nil {
				errorsChan <- model.CollectorError{
					SourceID:  src.ID,
					ErrorType: "fetch_error",
					Message:   err.Error(),
					Timestamp: time.Now(),
				}
				return
			}

			for _, item := range items {
				itemsChan <- item
			}
		}(src)
	}

	go func() {
		wg.Wait()
		close(itemsChan)
		close(errorsChan)
	}()

	var allItems []model.NewsItem
	for item := range itemsChan {
		allItems = append(allItems, item)
	}

	var allErrors []model.CollectorError
	for err := range errorsChan {
		allErrors = append(allErrors, err)
	}

	// Filter by age
	maxAge := time.Duration(cfg.Settings.MaxAgeHours) * time.Hour
	now := time.Now()
	var filteredItems []model.NewsItem
	for _, item := range allItems {
		if now.Sub(item.PublishedAt) <= maxAge {
			filteredItems = append(filteredItems, item)
		}
	}

	// Deduplicate
	deduplicatedItems := dedup.Deduplicate(filteredItems)

	outputData := model.NewsOutput{
		GeneratedAt:      now,
		PipelineVersion:  cfg.Metadata.Version,
		SourcesAttempted: sourcesAttempted,
		SourcesSucceeded: sourcesAttempted - len(allErrors),
		TotalRawItems:    len(allItems),
		Items:            deduplicatedItems,
		Errors:           allErrors,
	}

	err = output.WriteJSON(*outputPath, outputData)
	if err != nil {
		log.Fatalf("Error writing output: %v", err)
	}

	log.Printf("Collection complete: %d sources attempted, %d succeeded, %d items collected (%d after filter/dedup)", 
		outputData.SourcesAttempted, outputData.SourcesSucceeded, len(allItems), len(deduplicatedItems))
}
