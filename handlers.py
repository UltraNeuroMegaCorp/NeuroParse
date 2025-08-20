from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from config import CONTROL_CHAT_ID
from db import SessionLocalListener
from message_handler import handle_message


message_handler = MessageHandler(
    (filters.TEXT & (~filters.COMMAND)) | filters.VOICE,
    handle_message
)


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

    if update.message.chat.id != int(CONTROL_CHAT_ID):
        return
    db = SessionLocalListener()

    if not context.args:
        await update.message.reply_text("Используй: /target username")
        return

    context.bot_data["target_username"] = context.args[0].lstrip("@")
    target_username = context.bot_data.get("target_username")

    if message_handler not in app.handlers.get(0, []):
        app.add_handler(message_handler)

    await update.message.reply_text(f"Теперь слушаю только @{target_username}")
    db.close()


async def stop_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    app = context.application

    if update.message.chat.id != int(CONTROL_CHAT_ID):
        return

    target_username = context.bot_data.get("target_username")

    if target_username is None:
        await update.message.reply_text("⚠️ Целевой пользователь не выбран")
        return

    context.bot_data.pop("target_username", None)
    app.remove_handler(message_handler)
    await update.message.reply_text("⛔️ Прослушивание пользователя остановлено")


async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.id != int(CONTROL_CHAT_ID):
        return
    chat_id = update.message.chat.id
    await update.message.reply_text(f"Chat ID: {chat_id}")
