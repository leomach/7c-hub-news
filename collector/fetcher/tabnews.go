package fetcher

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"7c-hub-news/collector/config"
	"7c-hub-news/collector/model"
)

type TabNewsFetcher struct {
	client *http.Client
}

type tabNewsItem struct {
	Title       string    `json:"title"`
	Slug        string    `json:"slug"`
	PublishedAt time.Time `json:"published_at"`
	TabCoins    int       `json:"tabcoins"`
	Owner       string    `json:"owner_username"`
}

func NewTabNewsFetcher() *TabNewsFetcher {
	return &TabNewsFetcher{
		client: &http.Client{Timeout: 10 * time.Second},
	}
}

func (f *TabNewsFetcher) Fetch(ctx context.Context, source config.Source) ([]model.NewsItem, error) {
	strategy := "relevant"
	if val, ok := source.Config["strategy"].(string); ok {
		strategy = val
	}
	perPage := 15
	if val, ok := source.Config["per_page"].(int); ok {
		perPage = val
	}

	url := fmt.Sprintf("https://www.tabnews.com.br/api/v1/contents?strategy=%s&per_page=%d", strategy, perPage)
	resp, err := f.client.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var tabItems []tabNewsItem
	if err := json.NewDecoder(resp.Body).Decode(&tabItems); err != nil {
		return nil, err
	}

	var items []model.NewsItem
	for _, item := range tabItems {
		url := fmt.Sprintf("https://www.tabnews.com.br/%s/%s", item.Owner, item.Slug)
		items = append(items, model.NewsItem{
			ID:               fmt.Sprintf("tabnews-%s", item.Slug),
			Title:            item.Title,
			URL:              url,
			PublishedAt:      item.PublishedAt,
			SourceID:         source.ID,
			SourceName:       source.Name,
			SourceCategory:   source.Category,
			SourceLanguage:   source.Language,
			OriginalScore:    float64(item.TabCoins),
			ProcessingStatus: "raw",
		})
	}

	return items, nil
}
