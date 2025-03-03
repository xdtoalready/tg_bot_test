FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY bot.py .

# Открытие порта (используем 8000 по умолчанию)
EXPOSE 8000

# Метка для идентификации приложения
ARG app_id
LABEL app_id=$app_id

# Запуск приложения
# Переменные окружения должны быть переданы во время запуска контейнера
CMD ["python", "bot.py"]
