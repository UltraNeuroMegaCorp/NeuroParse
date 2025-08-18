from telegram.ext import ApplicationBuilder, MessageHandler, filters
from config import BOT_TOKEN
from db import Base, engine
from handlers import handle_message


def main():
    Base.metadata.create_all(bind=engine)

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 Бот запущен и пишет всё в базу...")
    app.run_polling()

if __name__ == "__main__":
    main()
