import httpx
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}/sendMessage"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def send_message(self, text: str):
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        with httpx.Client(timeout=15.0) as client:
            response = client.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()

    def send_bulletin(self, text: str):
        # Telegram has a 4096 character limit
        MAX_LENGTH = 4000
        
        if len(text) <= MAX_LENGTH:
            return self.send_message(text)
        
        # Split into parts if too long
        parts = []
        current_text = text
        while len(current_text) > 0:
            if len(current_text) <= MAX_LENGTH:
                parts.append(current_text)
                break
            
            # Try to split at a newline
            split_idx = current_text.rfind("\n", 0, MAX_LENGTH)
            if split_idx == -1:
                split_idx = MAX_LENGTH
            
            parts.append(current_text[:split_idx])
            current_text = current_text[split_idx:].strip()

        results = []
        for i, part in enumerate(parts):
            header = f"*7C Hub News ({i+1}/{len(parts)})*\n\n" if len(parts) > 1 else ""
            results.append(self.send_message(header + part))
            
        return results
