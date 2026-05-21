from google import genai
from google.genai import types
from processor.config.settings import Settings

class LLMClient:
    def __init__(self, settings: Settings):
        self.client = genai.Client(api_key=settings.llm_api_key)
        self.model_name = settings.llm_model

    def complete(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        full_prompt = f"{system_prompt}\n\n{prompt}"
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=full_prompt,
            config=types.GenerateContentConfig(temperature=0.3),
        )
        return response.text.strip()
