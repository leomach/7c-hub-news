from processor.models.news_item import NewsItem
from processor.llm.client import LLMClient

class Summarizer:
    def __init__(self, client: LLMClient):
        self.client = client
        with open("processor/prompts/summarize.txt", "r") as f:
            self.prompt_template = f.read()

    def summarize(self, item: NewsItem) -> NewsItem:
        # Use translated content if available
        title = item.title_pt or item.title
        summary = item.summary_pt or item.summary_original or ""

        prompt = self.prompt_template.format(
            title=title,
            summary=summary
        )

        try:
            response = self.client.complete(prompt)
            item.summary_pt = response
        except Exception as e:
            print(f"Error summarizing item {item.id}: {e}")
            if not item.summary_pt:
                item.summary_pt = item.summary_original[:280] if item.summary_original else ""
                
        return item
