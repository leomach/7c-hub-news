from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class NewsItem(BaseModel):
    id: str
    title: str
    url: str
    published_at: datetime
    source_id: str
    source_name: str
    source_category: str
    source_language: str
    original_score: float = 0.0
    summary_original: Optional[str] = None
    title_pt: Optional[str] = None
    summary_pt: Optional[str] = None
    llm_score: Optional[float] = None
    final_score: Optional[float] = None
    selected: bool = False
    processing_status: str = "raw"

class CollectorError(BaseModel):
    source_id: str
    error_type: str
    message: str
    timestamp: datetime

class NewsOutput(BaseModel):
    generated_at: datetime
    pipeline_version: str
    sources_attempted: int
    sources_succeeded: int
    total_raw_items: int
    items: List[NewsItem]
    errors: List[CollectorError]
