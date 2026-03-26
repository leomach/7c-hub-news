import os
import logging
import argparse
from dotenv import load_dotenv
from deliverer.telegram import TelegramBot

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Deliver the bulletin via Telegram")
    parser.add_argument("--input", default="output/bulletin.txt", help="Path to bulletin file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not found in environment")
        return

    if not os.path.exists(args.input):
        logger.error(f"Bulletin file not found: {args.input}")
        return

    with open(args.input, "r") as f:
        # Skip metadata header (split by ---)
        content = f.read()
        if "---" in content:
            content = content.split("---", 1)[1].strip()

    bot = TelegramBot(token, chat_id)
    
    try:
        bot.send_bulletin(content)
        logger.info("Bulletin delivered successfully via Telegram")
    except Exception as e:
        logger.error(f"Failed to deliver bulletin: {e}")
        exit(1)

if __name__ == "__main__":
    main()
