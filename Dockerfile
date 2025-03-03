FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY bot.py .

# Определение аргументов сборки с значениями по умолчанию
ARG TELEGRAM_BOT_TOKEN
ARG WEB3_URL=https://hermesx.ru
ARG PORT=8000

# Установка переменных окружения из аргументов сборки
ENV TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
ENV WEB3_URL=$WEB3_URL
ENV PORT=$PORT

# Открытие порта
EXPOSE $PORT

# Метка для идентификации приложения
ARG app_id
LABEL app_id=$app_id

# Запуск приложения
CMD ["python", "bot.py"]
