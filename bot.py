import os
import asyncio
import nest_asyncio
import threading
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Применяем nest_asyncio для корректной работы в одном event loop
nest_asyncio.apply()
load_dotenv()

# Настройка переменных окружения с проверкой на их доступность
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEB3_URL = os.getenv("WEB3_URL", "https://hermesx.ru")
PORT = int(os.getenv("PORT", "8000"))

# Вывод информации о конфигурации для диагностики
print(f"Конфигурация: WEB3_URL={WEB3_URL}, PORT={PORT}")
print(f"TELEGRAM_BOT_TOKEN: {'настроен' if TELEGRAM_BOT_TOKEN else 'НЕ НАСТРОЕН'}")

# Простой HTTP-сервер для health check
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")
        print("Получен health check запрос")

def start_health_server():
    try:
        server = HTTPServer(('0.0.0.0', PORT), HealthHandler)
        print(f"Starting health server on port {PORT}")
        server.serve_forever()
    except Exception as e:
        print(f"Ошибка при запуске HTTP-сервера: {e}")
        # Даже при ошибке HTTP-сервера не завершаем программу

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
    if not TELEGRAM_BOT_TOKEN:
        print("ПРЕДУПРЕЖДЕНИЕ: TELEGRAM_BOT_TOKEN не установлен, Telegram бот не будет запущен")
        # Бесконечный цикл для поддержания контейнера активным
        while True:
            await asyncio.sleep(60)
            print("Контейнер активен, но Telegram бот не работает из-за отсутствия токена")
    
    try:
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        print("Telegram бот запущен успешно")
        await application.run_polling(disable_signals=True)
    except Exception as e:
        print(f"Ошибка при запуске Telegram бота: {e}")
        # Бесконечный цикл для поддержания контейнера активным
        while True:
            await asyncio.sleep(60)
            print("Контейнер активен, но Telegram бот не работает из-за ошибки")

if __name__ == "__main__":
    # Запускаем HTTP-сервер для health check в отдельном потоке
    thread = threading.Thread(target=start_health_server, daemon=True)
    thread.start()
    
    # Запускаем Telegram-бота
    asyncio.run(run_telegram_bot())
