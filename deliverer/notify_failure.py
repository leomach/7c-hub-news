import os
import logging
from datetime import datetime
from deliverer.telegram import TelegramBot

def notify():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    run_url = os.getenv("GITHUB_RUN_URL", "URL not available")

    if not token or not chat_id:
        logger.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not found for notification")
        return

    bot = TelegramBot(token, chat_id)
    
    error_msg = f"⚠️ *7C Hub News — Erro no Pipeline*\n\n"
    error_msg += f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    error_msg += f"Status: Falha na execução do workflow.\n\n"
    error_msg += f"Verifique os logs do GitHub Actions:\n{run_url}"

    try:
        bot.send_message(error_msg)
        logger.info("Failure notification sent successfully")
    except Exception as e:
        logger.error(f"Failed to send failure notification: {e}")

if __name__ == "__main__":
    notify()
