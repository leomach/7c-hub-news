package config

import (
	"os"

	"gopkg.in/yaml.v3"
)

type Config struct {
	Metadata Metadata `yaml:"metadata"`
	Settings Settings `yaml:"settings"`
	Quotas   Quotas   `yaml:"quotas"`
	Sources  []Source `yaml:"sources"`
}

type Metadata struct {
	Version     string `yaml:"version"`
	LastUpdated string `yaml:"last_updated"`
}

type Settings struct {
	MaxAgeHours          int `yaml:"max_age_hours"`
	FetchTimeoutSeconds  int `yaml:"fetch_timeout_seconds"`
	MaxConcurrentFetches int `yaml:"max_concurrent_fetches"`
}

type Quotas struct {
	Global       int `yaml:"global"`
	National     int `yaml:"national"`
	Regional     int `yaml:"regional"`
	MinimumTotal int `yaml:"minimum_total"`
}

type Source struct {
	ID       string                 `yaml:"id"`
	Name     string                 `yaml:"name"`
	Type     string                 `yaml:"type"`
	Enabled  bool                   `yaml:"enabled"`
	Category string                 `yaml:"category"`
	Language string                 `yaml:"language"`
	Weight   float64                `yaml:"weight"`
	URL      string                 `yaml:"url,omitempty"`
	Config   map[string]interface{} `yaml:"config,omitempty"`
}

func LoadConfig(path string) (*Config, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	var cfg Config
	decoder := yaml.NewDecoder(f)
	err = decoder.Decode(&cfg)
	if err != nil {
		return nil, err
	}

	return &cfg, nil
}
