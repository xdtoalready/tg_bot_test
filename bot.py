import os
import asyncio
import nest_asyncio
from threading import Thread
from flask import Flask
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Разрешаем повторное использование event loop
nest_asyncio.apply()

# Загружаем переменные окружения из .env (если используете .env-файл)
load_dotenv()

# Переменные окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEB3_URL = os.getenv("WEB3_URL", "https://hermesx.ru")

# Создаём Flask-приложение
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

# Асинхронная функция, которая запускает Telegram-бот (Polling)
async def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    await application.run_polling()

# Функция для старта бота в отдельном потоке
def start_bot():
    asyncio.run(run_telegram_bot())

# Запускаем бота при старте приложения
Thread(target=start_bot, daemon=True).start()

# Если запускаем локально (например, python bot.py),
# Flask-приложение поднимется на порту 8000 (можно изменить при желании)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
