import json
from typing import List
from processor.models.news_item import NewsItem
from processor.llm.client import LLMClient

class Translator:
    def __init__(self, client: LLMClient):
        self.client = client
        with open("processor/prompts/translate.txt", "r") as f:
            self.prompt_template = f.read()

    def translate(self, item: NewsItem) -> NewsItem:
        if item.source_language == "pt":
            item.title_pt = item.title
            item.summary_pt = item.summary_original
            return item

        prompt = self.prompt_template.format(
            title=item.title,
            summary=item.summary_original or ""
        )
        
        try:
            response = self.client.complete(prompt)
            # Remove markdown code blocks if any
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
                
            data = json.loads(response)
            item.title_pt = data.get("title", item.title)
            item.summary_pt = data.get("summary", item.summary_original)
        except Exception as e:
            print(f"Error translating item {item.id}: {e}")
            item.title_pt = item.title
            item.summary_pt = item.summary_original
            
        return item
