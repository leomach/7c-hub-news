import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

from processor.config.settings import load_settings
from processor.models.news_item import NewsOutput, NewsItem
from processor.llm.client import LLMClient
from processor.llm.translator import Translator
from processor.llm.summarizer import Summarizer
from processor.pipeline.formatter import format_bulletin

load_dotenv()

def main():
    settings = load_settings()
    logging.basicConfig(level=settings.log_level)
    logger = logging.getLogger(__name__)

    if not os.path.exists(settings.input_file):
        logger.error(f"Input file not found: {settings.input_file}")
        return

    with open(settings.input_file, "r") as f:
        data = json.load(f)
        news_output = NewsOutput(**data)

    llm_client = LLMClient(settings)
    translator = Translator(llm_client)
    summarizer = Summarizer(llm_client)

    # Simplified selection for now (top items from each category up to quota)
    # This replaces the LLM Curatorship for this step as requested
    selected_items = []
    categories = ["global", "national", "regional"]
    
    # Map from sources.yaml names to Pydantic model names
    quota_map = {
        "global": settings.quotas.global_quota,
        "national": settings.quotas.national,
        "regional": settings.quotas.regional
    }

    for cat in categories:
        cat_items = [i for i in news_output.items if i.source_category == cat]
        # Sort by original score
        cat_items.sort(key=lambda x: x.original_score, reverse=True)
        selected_items.extend(cat_items[:quota_map[cat]])

    logger.info(f"Selected {len(selected_items)} items for processing")

    processed_items = []
    for item in selected_items:
        logger.info(f"Processing item: {item.title}")
        # Step 1: Translate
        item = translator.translate(item)
        # Step 2: Summarize
        item = summarizer.summarize(item)
        processed_items.append(item)

    # Generate bulletin
    bulletin_text = format_bulletin(processed_items, datetime.now())

    # Metadata header
    meta_header = f"# 7C Hub News — {datetime.now().strftime('%Y-%m-%d')}"

    meta_header += f"# Itens: {len(processed_items)} | LLM: {settings.llm_model}"

    meta_header += "---\n"

    # Save output
    os.makedirs(os.path.dirname(settings.output_file), exist_ok=True)
    with open(settings.output_file, "w") as f:
        f.write(meta_header + bulletin_text)

    logger.info(f"Bulletin generated and saved to {settings.output_file}")

if __name__ == "__main__":
    main()
