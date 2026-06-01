# Використовуємо офіційний легкий образ Python
FROM python:3.10-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Забороняємо Python писати файли .pyc на диск і буферизувати stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копіюємо файл залежностей та встановлюємо їх
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі інші файли проєкту (включаючи main.py та startup_planner.py)
COPY . /app/

# Відкриваємо порт 8000
EXPOSE 8000

# Команда для запуску веб-сервера uvicorn всередині контейнера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]