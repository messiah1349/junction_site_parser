import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER=os.getenv("POSTGRES_USER")
OPENAI_KEY=os.getenv("OPENAI_KEY")
