from flask import Flask
import random
from datetime import datetime, timedelta
import os
import re

app = Flask(__name__)


cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada', 'Toyota']
cats_list = ['сфинкс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
counter_visits = 0
words_list = None


def load_words_from_book():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

    words = []
    try:
        with open(BOOK_FILE, 'r', encoding='utf-8') as book:
            text = book.read()
            words = re.findall(r'[а-яА-Яa-zA-Z]+', text)
    except FileNotFoundError:
        print("Файл war_and_peace.txt не найден")
        words = ['мир', 'война', 'человек', 'жизнь', 'счастье']

    return words



words_list = load_words_from_book()


@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'


@app.route('/cars')
def cars():
    return ', '.join(cars_list)


@app.route('/cats')
def cats():
    return random.choice(cats_list)


@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.now().strftime('%H:%M:%S')
    return f'Точное время: {current_time}'


@app.route('/get_time/future')
def get_time_future():
    current_time_after_hour = (datetime.now() + timedelta(hours=1)).strftime('%H:%M:%S')
    return f'Точное время через час будет {current_time_after_hour}'


@app.route('/get_random_word')
def get_random_word():
    return random.choice(words_list)


@app.route('/counter')
def counter():
    global counter_visits
    counter_visits += 1
    return str(counter_visits)


if __name__ == '__main__':
    app.run(debug=True)