import os
import asyncio
import nest_asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Применяем nest_asyncio для корректной работы в одном event loop
nest_asyncio.apply()
load_dotenv()

# Получаем переменные окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEB3_URL = os.getenv("WEB3_URL", "https://hermesx.ru")
# Порт для health-сервера, по умолчанию 8000
PORT = int(os.getenv("PORT", "8000"))

# Минимальный HTTP-сервер для health check
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

def start_health_server():
    server = HTTPServer(('0.0.0.0', PORT), HealthHandler)
    print(f"Starting health server on port {PORT}")
    server.serve_forever()

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Открыть миниапп Web3", url=WEB3_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Нажми кнопку ниже, чтобы открыть мини-приложение Web3.",
        reply_markup=reply_markup
    )

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Используйте /start для начала.")

# Запуск Telegram-бота
async def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    await application.run_polling(disable_signals=True)

if __name__ == "__main__":
    # Запускаем HTTP-сервер для health check в отдельном потоке
    threading.Thread(target=start_health_server, daemon=True).start()
    # Запускаем Telegram-бота
    asyncio.run(run_telegram_bot())
