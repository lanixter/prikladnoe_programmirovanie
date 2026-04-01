from flask import Flask
from datetime import datetime
import os

app = Flask(__name__)

WEEKDAYS_RU = ('понедельника', 'вторника', 'среды', 'четверга', 'пятницы', 'субботы', 'воскресенья')


@app.route('/hello-world/<name>')
def hello_world(name):
    weekday_num = datetime.today().weekday()
    weekday_name = WEEKDAYS_RU[weekday_num]
    return f'Привет, {name}. Хорошего {weekday_name}!'


@app.route('/max_number/<path:numbers>')
def max_number(numbers):
    parts = numbers.split('/')
    max_value = None
    for part in parts:
        try:
            num = int(part)
            if max_value is None or num > max_value:
                max_value = num
        except ValueError:
            continue
    if max_value is None:
        return 'Не передано ни одного числа'
    return f'Максимальное переданное число <i>{max_value}</i>'


@app.route('/preview/<int:size>/<path:relative_path>')
def preview_file(size, relative_path):
    abs_path = os.path.abspath(relative_path)
    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            result_text = f.read(size)
        result_size = len(result_text)
        return f'<b>{abs_path}</b> {result_size}<br>{result_text}'
    except FileNotFoundError:
        return f'<b>Ошибка:</b> Файл {abs_path} не найден'
    except Exception as e:
        return f'<b>Ошибка:</b> {str(e)}'


storage = {}


@app.route('/add/<date>/<int:number>')
def add_expense(date, number):
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:8])
    storage.setdefault(year, {}).setdefault(month, 0)
    storage[year][month] += number
    return f'Добавлена трата {number} руб. за {day}.{month}.{year}'


@app.route('/calculate/<int:year>')
def calculate_year(year):
    if year not in storage:
        return f'Трат за {year} год не найдено'
    total = sum(storage[year].values())
    return f'Суммарные траты за {year} год: {total} руб.'


@app.route('/calculate/<int:year>/<int:month>')
def calculate_month(year, month):
    if year not in storage or month not in storage[year]:
        return f'Трат за {month}.{year} не найдено'
    total = storage[year][month]
    return f'Суммарные траты за {month}.{year}: {total} руб.'


if __name__ == '__main__':
    app.run(debug=True)