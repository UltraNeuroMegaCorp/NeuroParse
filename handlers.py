import json

from telegram import Update
from telegram.ext import ContextTypes
from db_handlers import DbHandler
from db import SessionLocal


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    db_handler = DbHandler(db)

    msg = update.message
    if not msg:
        return

    chat_title = msg.chat.title
    username = msg.from_user.username or msg.from_user.first_name
    text = msg.text
    message_time = msg.date

    reply_to_user_username = None
    reply_to_text = None

    if msg.reply_to_message:
        reply_user = msg.reply_to_message.from_user
        if reply_user:
            reply_to_user_username = reply_user.username or reply_user.first_name
        reply_to_text = msg.reply_to_message.text

    db_handler.add_message(
        chat_title, username,
        text, message_time,
        reply_to_user_username, reply_to_text
    )

    print(f"[{chat_title}] {username}: {text}")

    db.close()
