from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from config import CONTROL_CHAT_ID, TARGET_CHAT_ID
from db_handlers import DbHandler
from db import SessionLocalMessage, SessionLocalListener
from models import Message, Listener

TARGET_USERNAME = None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TARGET_USERNAME

    msg = update.message
    if not msg:
        return

    if msg.chat.id != int(TARGET_CHAT_ID):
        return

    chat_title = msg.chat.title
    username = msg.from_user.username or msg.from_user.first_name
    text = msg.text
    message_time = msg.date

    if TARGET_USERNAME:
        if username != TARGET_USERNAME:
            return
        db = SessionLocalListener()
        db_handler = DbHandler(db, Listener)
    else:
        db = SessionLocalMessage()
        db_handler = DbHandler(db, Message)

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
    app = context.application

    global TARGET_USERNAME

    if update.message.chat.id != int(CONTROL_CHAT_ID):
        return
    db = SessionLocalListener()

    if not context.args:
        await update.message.reply_text("Используй: /target username")
        return

    username = context.args[0].lstrip("@")
    TARGET_USERNAME = username

    if message_handler not in app.handlers.get(0, []):
        app.add_handler(message_handler)

    await update.message.reply_text(f"Теперь слушаю только @{username}")
    db.close()


async def stop_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TARGET_USERNAME
    app = context.application

    if update.message.chat.id != int(CONTROL_CHAT_ID):
        return

    if TARGET_USERNAME is None:
        await update.message.reply_text("⚠️ Целевой пользователь не выбран")
        return

    TARGET_USERNAME = None
    app.remove_handler(message_handler)
    await update.message.reply_text("⛔️ Прослушивание пользователя остановлено")



async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.id != int(CONTROL_CHAT_ID):
        return
    chat_id = update.message.chat.id
    await update.message.reply_text(f"Chat ID: {chat_id}")
