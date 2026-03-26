from typing import Dict
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

class Quotas(BaseModel):
    global_quota: int = 3
    national: int = 2
    regional: int = 1
    minimum_total: int = 3

class Settings(BaseSettings):
    llm_provider: str = "gemini"
    llm_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    llm_model: str = "gemini-1.5-flash"
    llm_api_key: str
    
    input_file: str = "output/news.json"
    output_file: str = "output/bulletin.txt"
    log_level: str = "INFO"
    
    # Quotas from sources.yaml will be loaded here
    quotas: Quotas = Quotas()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

def load_settings(sources_yaml_path: str = "sources.yaml") -> Settings:
    with open(sources_yaml_path, "r") as f:
        config = yaml.safe_load(f)
    
    q = config.get("quotas", {})
    quotas = Quotas(
        global_quota=q.get("global", 3),
        national=q.get("national", 2),
        regional=q.get("regional", 1),
        minimum_total=q.get("minimum_total", 3)
    )
    
    settings = Settings(quotas=quotas)
    return settings
