import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MESSAGE_DB_PATH = os.getenv("MESSAGE_DB_PATH", "")
LISTENER_DB_PATH = os.getenv("LISTENER_DB_PATH", "")
CONTROL_CHAT_ID = os.getenv("CONTROL_CHAT_ID", "")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID", "")
