from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN
from db import init_db
from handlers import listen_command, target_command, stop_target, get_chat_id


def main():
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("listen", listen_command))
    app.add_handler(CommandHandler("target", target_command))
    app.add_handler(CommandHandler("stop_target", stop_target))
    app.add_handler(CommandHandler("get_chat_id", get_chat_id))

    print("🤖 Бот запущен и пишет всё в базу...")
    app.run_polling()


if __name__ == "__main__":
    main()
