# plot.py
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# Убедимся, что директория logs существует
if not os.path.exists('logs'):
    os.makedirs('logs')

# Путь к файлу metric_log.csv
metric_log_file = 'logs/metric_log.csv'

# Убедимся, что директория для графиков существует
plots_dir = 'plot'
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

while True:
    try:
        # Проверяем, существует ли файл и не пуст ли он
        if os.path.isfile(metric_log_file) and os.path.getsize(metric_log_file) > 0:
            # Читаем данные из CSV файла
            data = pd.read_csv(metric_log_file, header=None, names=['id', 'y_true', 'y_pred', 'absolute_error'])
            
            # Строим график y_true vs y_pred
            plt.figure()
            plt.scatter(data['y_true'], data['y_pred'], alpha=0.7)
            plt.plot([data['y_true'].min(), data['y_true'].max()],
                     [data['y_true'].min(), data['y_true'].max()],
                     'r--', lw=2)
            plt.xlabel('Истинные значения (y_true)')
            plt.ylabel('Предсказанные значения (y_pred)')
            plt.title('Сравнение истинных и предсказанных значений')
            plt.grid(True)
            plt.savefig(os.path.join(plots_dir, 'y_true_vs_y_pred.png'))
            plt.close()

            # Строим график абсолютной ошибки по мере поступления данных
            plt.figure()
            plt.plot(data['id'], data['absolute_error'], marker='o')
            plt.xlabel('ID сообщения')
            plt.ylabel('Абсолютная ошибка')
            plt.title('Изменение абсолютной ошибки со временем')
            plt.grid(True)
            plt.savefig(os.path.join(plots_dir, 'absolute_error_over_time.png'))
            plt.close()

            # Строим гистограмму распределения абсолютной ошибки
            plt.figure()
            plt.hist(data['absolute_error'], bins=30, alpha=0.7, color='blue')
            plt.xlabel('Абсолютная ошибка')
            plt.ylabel('Частота')
            plt.title('Распределение абсолютной ошибки')
            plt.grid(True)
            plt.savefig('logs/error_distribution.png')  # Сохраняем в logs
            plt.close()

            print('Графики обновлены.')
        else:
            print('Файл метрик не найден или пуст. Ожидание данных...')

        # Ждем перед следующей проверкой
        time.sleep(5)
    except Exception as e:
        print(f'Ошибка при обновлении графиков: {e}')
        # Ждем перед повторной попыткой в случае ошибки
        time.sleep(5)
