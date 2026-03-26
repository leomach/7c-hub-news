package dedup

import (
	"strings"
	"7c-hub-news/collector/model"
)

func Deduplicate(items []model.NewsItem) []model.NewsItem {
	seen := make(map[string]bool)
	var result []model.NewsItem

	for _, item := range items {
		url := normalizeURL(item.URL)
		if !seen[url] {
			seen[url] = true
			result = append(result, item)
		}
	}

	return result
}

func normalizeURL(url string) string {
	url = strings.Split(url, "?")[0]
	url = strings.TrimSuffix(url, "/")
	return strings.ToLower(url)
}
