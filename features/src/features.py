import pika
import numpy as np
import json
from sklearn.datasets import load_diabetes
from datetime import datetime
import time
import logging

# Настройка ведения журналов
logging.basicConfig(level=logging.INFO)

# Функция для обновления гистограммы
def update_histogram(data):
    # Здесь можно реализовать логику обновления гистограммы
    logging.info(f"Гистограмма обновлена: {data}")

# Создаём бесконечный цикл для отправки сообщений в очередь
while True:
    try:
        # Загружаем датасет о диабете
        X, y = load_diabetes(return_X_y=True)
        # Формируем случайный индекс строки
        random_row = np.random.randint(0, X.shape[0]-1)

        # Создаём подключение по адресу rabbitmq
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Создаём очередь y_true
        channel.queue_declare(queue='y_true')
        # Создаём очередь features
        channel.queue_declare(queue='features')

        # Генерируем уникальный идентификатор
        message_id = datetime.timestamp(datetime.now())

        # Создаём сообщения с идентификатором
        message_y_true = {
            'id': message_id,
            'body': y[random_row]
        }
        message_features = {
            'id': message_id,
            'body': list(X[random_row])
        }

        # Публикуем сообщение в очередь y_true
        channel.basic_publish(exchange='',
                              routing_key='y_true',
                              body=json.dumps(message_y_true))
        logging.info('Сообщение с правильным ответом отправлено в очередь')

        # Публикуем сообщение в очередь features
        channel.basic_publish(exchange='',
                              routing_key='features',
                              body=json.dumps(message_features))
        logging.info('Сообщение с вектором признаков отправлено в очередь')

        # Обновляем гистограмму
        update_histogram(list(X[random_row]))

        # Закрываем подключение
        connection.close()

        # Задержка перед следующей итерацией
        time.sleep(10)

    except Exception as e:
        logging.error(f'Не удалось подключиться к очереди: {e}')
