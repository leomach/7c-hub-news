package fetcher

import (
	"context"
	"collector/config"
	"collector/model"
)

type Fetcher interface {
	Fetch(ctx context.Context, source config.Source) ([]model.NewsItem, error)
}
