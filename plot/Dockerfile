# plot.Dockerfile
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app
COPY ./src ./
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Команда для запуска скрипта
CMD ["python", "./plot.py"]


