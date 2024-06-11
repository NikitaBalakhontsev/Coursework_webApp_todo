FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска приложения с Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "back:app"]