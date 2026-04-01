from flask import Flask
from datetime import datetime

app = Flask(__name__)

WEEKDAYS_RU = ('понедельника', 'вторника', 'среды', 'четверга', 'пятницы', 'субботы', 'воскресенья')

@app.route('/hello-world/<name>')
def hello_world(name):
    weekday_num = datetime.today().weekday()
    weekday_name = WEEKDAYS_RU[weekday_num]
    return f'Привет, {name}. Хорошего {weekday_name}!'

if __name__ == '__main__':
    app.run(debug=True)