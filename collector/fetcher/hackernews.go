package fetcher

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
	"time"

	"7c-hub-news/collector/config"
	"7c-hub-news/collector/model"
)

type HNFetcher struct {
	client *http.Client
}

type hnItem struct {
	ID    int    `json:"id"`
	Title string `json:"title"`
	URL   string `json:"url"`
	Time  int64  `json:"time"`
	Score int    `json:"score"`
	Type  string `json:"type"`
}

func NewHNFetcher() *HNFetcher {
	return &HNFetcher{
		client: &http.Client{Timeout: 10 * time.Second},
	}
}

func (f *HNFetcher) Fetch(ctx context.Context, source config.Source) ([]model.NewsItem, error) {
	resp, err := f.client.Get("https://hacker-news.firebaseio.com/v0/topstories.json")
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var ids []int
	if err := json.NewDecoder(resp.Body).Decode(&ids); err != nil {
		return nil, err
	}

	limit := 30
	if val, ok := source.Config["top_stories_limit"].(int); ok {
		limit = val
	}
	if len(ids) > limit {
		ids = ids[:limit]
	}

	var items []model.NewsItem
	var mu sync.Mutex
	var wg sync.WaitGroup

	for _, id := range ids {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			item, err := f.fetchItem(id)
			if err != nil || item.Type != "story" || item.URL == "" {
				return
			}

			mu.Lock()
			items = append(items, model.NewsItem{
				ID:               fmt.Sprintf("hn-%d", item.ID),
				Title:            item.Title,
				URL:              item.URL,
				PublishedAt:      time.Unix(item.Time, 0),
				SourceID:         source.ID,
				SourceName:       source.Name,
				SourceCategory:   source.Category,
				SourceLanguage:   source.Language,
				OriginalScore:    float64(item.Score),
				ProcessingStatus: "raw",
			})
			mu.Unlock()
		}(id)
	}

	wg.Wait()
	return items, nil
}

func (f *HNFetcher) fetchItem(id int) (*hnItem, error) {
	url := fmt.Sprintf("https://hacker-news.firebaseio.com/v0/item/%d.json", id)
	resp, err := f.client.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var item hnItem
	if err := json.NewDecoder(resp.Body).Decode(&item); err != nil {
		return nil, err
	}
	return &item, nil
}
