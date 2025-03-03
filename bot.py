import os
import asyncio
import nest_asyncio
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Применяем nest_asyncio для корректной работы в одном event loop
nest_asyncio.apply()
load_dotenv()

# Вывод всех переменных окружения для диагностики
print("===== ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ =====")
for key, value in os.environ.items():
    if key in ['TELEGRAM_BOT_TOKEN', 'WEB3_URL', 'PORT']:
        masked_value = value[:4] + '****' if key == 'TELEGRAM_BOT_TOKEN' else value
        print(f"{key}: {masked_value}")
print("================================")

# Настройка переменных с резервными значениями
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEB3_URL = os.getenv("WEB3_URL", "https://hermesx.ru")
PORT = int(os.getenv("PORT", "8000"))

# Простой HTTP-сервер для health check
class HealthHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.protocol_version = 'HTTP/1.1'
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")
        print(f"Health check запрос обработан на порту {PORT}")

def start_health_server():
    try:
        server = HTTPServer(('0.0.0.0', PORT), HealthHandler)
        print(f"Health server запущен на порту {PORT}")
        server.serve_forever()
    except Exception as e:
        print(f"Ошибка при запуске HTTP-сервера: {e}")
        # Продолжаем работу даже при ошибке HTTP-сервера

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Открыть миниапп Web3", url=WEB3_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Нажми кнопку ниже, чтобы открыть мини-приложение Web3.",
        reply_markup=reply_markup
    )
    print(f"Обработана команда /start от пользователя {update.effective_user.id}")

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Используйте /start для начала.")
    print(f"Обработана команда /help от пользователя {update.effective_user.id}")

# Функция для непрерывной работы контейнера
async def keep_alive():
    while True:
        print("Контейнер активен...")
        await asyncio.sleep(60)

# Запуск Telegram-бота
async def run_telegram_bot():
    if not TELEGRAM_BOT_TOKEN:
        print("ОШИБКА: TELEGRAM_BOT_TOKEN не установлен, бот не запущен!")
        await keep_alive()
        return
    
    try:
        print("Пытаемся запустить Telegram бота...")
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        print("Telegram бот настроен и готов к запуску")
        
        # Запускаем бота с обработкой ошибок
        try:
            print("Запускаем polling...")
            await application.run_polling(drop_pending_updates=True)
        except Exception as e:
            print(f"Ошибка при работе бота: {e}")
            await keep_alive()
    except Exception as e:
        print(f"Ошибка при инициализации бота: {e}")
        await keep_alive()

if __name__ == "__main__":
    # Запускаем HTTP-сервер для health check в отдельном потоке
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    print("Health server thread запущен")
    
    # Запускаем Telegram-бота
    print("Запускаем основной процесс Telegram-бота")
    try:
        asyncio.run(run_telegram_bot())
    except Exception as e:
        print(f"Критическая ошибка в основном процессе: {e}")
        # Если основной процесс завершился с ошибкой, 
        # запускаем бесконечный цикл для поддержания контейнера
        while True:
            print("Контейнер поддерживается в активном состоянии после сбоя")
            time.sleep(60)
