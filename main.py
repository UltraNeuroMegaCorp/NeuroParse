from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from db import Base, engine
from handlers import listen_command, target_command



def main():
    Base.metadata.create_all(bind=engine)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("listen", listen_command))
    app.add_handler(CommandHandler("target", target_command))

    print("🤖 Бот запущен и пишет всё в базу...")
    app.run_polling()


if __name__ == "__main__":
    main()
