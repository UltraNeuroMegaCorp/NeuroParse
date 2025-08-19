import json

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from config import CONTROL_CHAT_ID
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

message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)


async def listen_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.id != int(CONTROL_CHAT_ID):
        return
    app = context.application
    args = context.args

    if not args:
        await update.message.reply_text("Используй: /listen on или /listen off")
        return

    if args[0].lower() == "on":
        if message_handler not in app.handlers.get(0, []):
            app.add_handler(message_handler)
            await update.message.reply_text("✅ Слушатель включен")
        else:
            await update.message.reply_text("⚠️ Слушатель уже включен")
    elif args[0].lower() == "off":
        if message_handler in app.handlers.get(0, []):
            app.remove_handler(message_handler)
            await update.message.reply_text("⛔️ Слушатель выключен")
        else:
            await update.message.reply_text("⚠️ Слушатель уже выключен")


async def target_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.id != int(CONTROL_CHAT_ID):
        return
    db = SessionLocal()

    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)

    db_handler = DbHandler(db)

    if not context.args:
        await update.message.reply_text("Используй: /target username")
        return

    username = context.args[0].lstrip("@")
    await update.message.reply_text(f"Теперь слушаю только @{username}")
    db.close()


async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.id != int(CONTROL_CHAT_ID):
        return
    chat_id = update.message.chat.id
    await update.message.reply_text(f"Chat ID: {chat_id}")