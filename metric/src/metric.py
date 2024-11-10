import pika
import json
import logging
import csv

# Настройка логирования
logging.basicConfig(filename='labels_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Создаём пустой словарь для хранения истинных меток и предсказаний
cache = {'y_true': {}, 'y_pred': {}}

# Функция для записи в файл metric_log.csv
def write_to_csv(message_id, y_true, y_pred):
    absolute_error = abs(y_true - y_pred)
    with open('metric_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([message_id, y_true, y_pred, absolute_error])

try:
    # Создаём подключение к серверу на локальном хосте
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очередь y_true
    channel.queue_declare(queue='y_true')
    # Объявляем очередь y_pred
    channel.queue_declare(queue='y_pred')

    # Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):
        message = json.loads(body)
        queue_name = method.routing_key
        message_id = message['id']
        value = message['body']
        
        print(f'Из очереди {queue_name} получено сообщение ID = {message_id}, значение = {value}')
        # Записываем информацию в лог
        logging.info(f'Из очереди {queue_name} получено сообщение ID = {message_id}, значение = {value}')

        # Сохраняем значение в кэш
        cache[queue_name][message_id] = value

        # Проверяем, есть ли сопоставление по message_id в обеих очередях
        if message_id in cache['y_true'] and message_id in cache['y_pred']:
            y_true = cache['y_true'].pop(message_id)
            y_pred = cache['y_pred'].pop(message_id)
            write_to_csv(message_id, y_true, y_pred)

    # Извлекаем сообщение из очереди y_true
    channel.basic_consume(
        queue='y_true',
        on_message_callback=callback,
        auto_ack=True
    )
    # Извлекаем сообщение из очереди y_pred
    channel.basic_consume(
        queue='y_pred',
        on_message_callback=callback,
        auto_ack=True
    )

    # Запускаем режим ожидания прихода сообщений
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()
except Exception as e:
    print(f'Не удалось подключиться к очереди: {e}')
