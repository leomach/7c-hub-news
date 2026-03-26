package fetcher

import (
	"context"
	"fmt"
	"time"

	"7c-hub-news/collector/config"
	"7c-hub-news/collector/model"

	"github.com/mmcdole/gofeed"
)

type RSSFetcher struct {
	parser *gofeed.Parser
}

func NewRSSFetcher() *RSSFetcher {
	return &RSSFetcher{
		parser: gofeed.NewParser(),
	}
}

func (f *RSSFetcher) Fetch(ctx context.Context, source config.Source) ([]model.NewsItem, error) {
	feed, err := f.parser.ParseURLWithContext(source.URL, ctx)
	if err != nil {
		return nil, err
	}

	var items []model.NewsItem
	limit := 10
	if val, ok := source.Config["max_items"].(int); ok {
		limit = val
	}

	for i, entry := range feed.Items {
		if i >= limit {
			break
		}

		pubDate := time.Now()
		if entry.PublishedParsed != nil {
			pubDate = *entry.PublishedParsed
		} else if entry.UpdatedParsed != nil {
			pubDate = *entry.UpdatedParsed
		}

		id := entry.GUID
		if id == "" {
			id = entry.Link
		}

		items = append(items, model.NewsItem{
			ID:               fmt.Sprintf("%s-%s", source.ID, id),
			Title:            entry.Title,
			URL:              entry.Link,
			PublishedAt:      pubDate,
			SourceID:         source.ID,
			SourceName:       source.Name,
			SourceCategory:   source.Category,
			SourceLanguage:   source.Language,
			OriginalScore:    1.0, // Default for RSS
			SummaryOriginal:  entry.Description,
			ProcessingStatus: "raw",
		})
	}

	return items, nil
}
