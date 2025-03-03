import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

nest_asyncio.apply()
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEB3_URL = os.getenv("WEB3_URL", "https://hermesx.ru")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Открыть миниапп Web3", url=WEB3_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми кнопку ниже, чтобы открыть мини-приложение Web3.",
                                      reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Используйте /start для начала.")

async def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    # disable_signals=True безопасно, если бот запускается в отдельном процессе
    await application.run_polling(disable_signals=True)

if __name__ == "__main__":
    asyncio.run(run_telegram_bot())
