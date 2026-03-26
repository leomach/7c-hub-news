package fetcher

import (
	"context"
	"7c-hub-news/collector/config"
	"7c-hub-news/collector/model"
)

type Fetcher interface {
	Fetch(ctx context.Context, source config.Source) ([]model.NewsItem, error)
}
