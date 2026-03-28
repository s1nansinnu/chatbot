import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_NAME = 'gemini-1.5-flash'
MAX_TOKENS = 3000
MAX_HISTORY_MESSAGES = 10
DB_PATH = 'chat_history.db'