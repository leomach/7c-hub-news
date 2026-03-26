import google.generativeai as genai
from processor.config.settings import Settings

class LLMClient:
    def __init__(self, settings: Settings):
        genai.configure(api_key=settings.llm_api_key)
        self.model = genai.GenerativeModel(settings.llm_model)

    def complete(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        # For Gemini, system instruction is passed during model init usually, 
        # but we can also prepend it to the prompt.
        full_prompt = f"{system_prompt}\n\n{prompt}"
        response = self.model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3
            )
        )
        return response.text.strip()
