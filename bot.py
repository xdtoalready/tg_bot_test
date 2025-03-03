import os
import asyncio
import nest_asyncio
from threading import Thread
from flask import Flask
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Применяем nest_asyncio для корректной работы в одном event loop
nest_asyncio.apply()

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем значения переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEB3_URL = os.getenv("WEB3_URL", "https://hermesx.ru")

# Создаем Flask-приложение
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from HermesX bot with Flask!"

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

# Асинхронная функция запуска Telegram-бота через polling с отключенными сигналами
async def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    await application.run_polling(disable_signals=True)

# Функция для запуска бота в отдельном потоке
def start_bot():
    asyncio.run(run_telegram_bot())

# Запускаем бота в фоновом потоке
Thread(target=start_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
