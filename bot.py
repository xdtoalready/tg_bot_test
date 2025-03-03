import os
import asyncio
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Применяем nest_asyncio для корректной работы в одном event loop
nest_asyncio.apply()

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем значения переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEB3_URL = os.getenv("WEB3_URL")  # URL вашего мини-приложения Web3

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Открыть миниапп Web3", url=WEB3_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Нажми кнопку ниже, чтобы открыть мини-приложение Web3.",
        reply_markup=reply_markup
    )

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Используйте /start для начала.")

# Основная функция запуска бота
async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
