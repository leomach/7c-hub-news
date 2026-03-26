package model

import "time"

type NewsItem struct {
	ID              string    `json:"id"`
	Title           string    `json:"title"`
	URL             string    `json:"url"`
	PublishedAt     time.Time `json:"published_at"`
	SourceID        string    `json:"source_id"`
	SourceName      string    `json:"source_name"`
	SourceCategory  string    `json:"source_category"`
	SourceLanguage  string    `json:"source_language"`
	OriginalScore   float64   `json:"original_score"`
	SummaryOriginal string    `json:"summary_original"`
	TitlePT         *string   `json:"title_pt"`
	SummaryPT       *string   `json:"summary_pt"`
	LLMScore        *float64  `json:"llm_score"`
	FinalScore      *float64  `json:"final_score"`
	Selected        bool      `json:"selected"`
	ProcessingStatus string   `json:"processing_status"`
}

type NewsOutput struct {
	GeneratedAt      time.Time   `json:"generated_at"`
	PipelineVersion  string      `json:"pipeline_version"`
	SourcesAttempted int         `json:"sources_attempted"`
	SourcesSucceeded int         `json:"sources_succeeded"`
	TotalRawItems    int         `json:"total_raw_items"`
	Items            []NewsItem  `json:"items"`
	Errors           []CollectorError `json:"errors"`
}

type CollectorError struct {
	SourceID  string    `json:"source_id"`
	ErrorType string    `json:"error_type"`
	Message   string    `json:"message"`
	Timestamp time.Time `json:"timestamp"`
}
