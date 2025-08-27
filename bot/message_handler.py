import os
import uuid

import requests
from telegram import Update
from telegram.ext import ContextTypes

from config import TARGET_CHAT_IDS, MODEL_API_URL
from db import SessionLocalListener, SessionLocalMessage
from db_handlers import DbHandler
from models import Listener, Message

VOICES_DIR = "voice_messages"
os.makedirs(VOICES_DIR, exist_ok=True)
TARGET_CHAT_IDS = [int(x) for x in TARGET_CHAT_IDS.split(",")]


def save_message(msg, text, db_model):
    db = SessionLocalListener() if db_model is Listener else SessionLocalMessage()
    db_handler = DbHandler(db, db_model)

    reply_to_user_username = None
    reply_to_text = None

    if msg.reply_to_message:
        reply_user = msg.reply_to_message.from_user
        if reply_user:
            reply_to_user_username = reply_user.username or reply_user.first_name
        reply_to_text = (
            msg.reply_to_message.text
            or msg.reply_to_message.caption
        )

    db_handler.add_message(
        msg.chat.title,
        msg.from_user.username or msg.from_user.first_name,
        text,
        msg.date,
        reply_to_user_username,
        reply_to_text,
    )
    db.close()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or msg.chat.id not in TARGET_CHAT_IDS:
        return

    username = msg.from_user.username or msg.from_user.first_name
    target_username = context.bot_data.get("target_username")

    if target_username and username != target_username:
        return

    if msg.text:
        text = msg.text
    elif msg.voice:
        file_id = msg.voice.file_id
        file = await context.bot.get_file(file_id)
        file_path = os.path.join(VOICES_DIR, f"{uuid.uuid4()}.ogg")

        await file.download_to_drive(file_path)
        print(f"🎤 Голосовое сохранено: {file_path}")

        with open(file_path, "rb") as f:
            response = requests.post(MODEL_API_URL, files={"file": f})

        if response.status_code == 200:
            text = response.json().get("text", "").strip()
            print(f"✅ Распознанный текст: {text}")
        else:
            print(f"❌ Ошибка API: {response.text}")
            return

        os.remove(file_path)
        print(f"🗑️ Файл удалён: {file_path}")
    else:
        return

    db_model = Listener if target_username else Message
    save_message(msg, text, db_model)

    print(f"[{msg.chat.title}] {username}: {text}")
