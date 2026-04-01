from flask import Flask, render_template_string, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Email, Regexp, ValidationError
import subprocess
import shlex

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-for-csrf'


# ========== Задача 2: Создание валидатора ==========
def phone_length(min_length: int, max_length: int, message: str = None):
    """Функциональный валидатор"""

    def _phone_length(form, field):
        if field.data:
            phone_str = str(field.data)
            if len(phone_str) < min_length or len(phone_str) > max_length:
                if message:
                    raise ValidationError(message)
                else:
                    raise ValidationError(f'Номер телефона должен содержать от {min_length} до {max_length} цифр')

    return _phone_length


class PhoneLength:
    """Классовый валидатор"""

    def __init__(self, min_length: int, max_length: int, message: str = None):
        self.min_length = min_length
        self.max_length = max_length
        self.message = message

    def __call__(self, form, field):
        if field.data:
            phone_str = str(field.data)
            if len(phone_str) < self.min_length or len(phone_str) > self.max_length:
                if self.message:
                    raise ValidationError(self.message)
                else:
                    raise ValidationError(
                        f'Номер телефона должен содержать от {self.min_length} до {self.max_length} цифр')


# ========== Задача 1: Форма с валидаторами ==========
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        InputRequired(message='Email обязателен для заполнения'),
        Email(message='Введите корректный email')
    ])

    phone = StringField('Phone', validators=[
        InputRequired(message='Телефон обязателен для заполнения'),
        Regexp(r'^\d+$', message='Телефон должен содержать только цифры'),
        PhoneLength(min_length=10, max_length=10, message='Телефон должен содержать ровно 10 цифр')
    ])

    name = StringField('Name', validators=[
        InputRequired(message='Имя обязательно для заполнения')
    ])

    address = StringField('Address', validators=[
        InputRequired(message='Адрес обязателен для заполнения')
    ])

    index = StringField('Index', validators=[
        InputRequired(message='Индекс обязателен для заполнения'),
        Regexp(r'^\d+$', message='Индекс должен содержать только цифры')
    ])

    comment = TextAreaField('Comment', validators=[])


HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Регистрация</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        .error { color: red; font-size: 0.9em; }
        input, textarea { margin: 5px 0; padding: 5px; width: 300px; }
        button { padding: 10px 20px; background: blue; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Регистрация</h1>
    <form method="POST">
        {{ form.csrf_token }}

        <div>
            {{ form.email.label }}<br>
            {{ form.email(size=40) }}<br>
            {% for error in form.email.errors %}
                <span class="error">{{ error }}</span><br>
            {% endfor %}
        </div>

        <div>
            {{ form.phone.label }}<br>
            {{ form.phone(size=40) }}<br>
            {% for error in form.phone.errors %}
                <span class="error">{{ error }}</span><br>
            {% endfor %}
        </div>

        <div>
            {{ form.name.label }}<br>
            {{ form.name(size=40) }}<br>
            {% for error in form.name.errors %}
                <span class="error">{{ error }}</span><br>
            {% endfor %}
        </div>

        <div>
            {{ form.address.label }}<br>
            {{ form.address(size=40) }}<br>
            {% for error in form.address.errors %}
                <span class="error">{{ error }}</span><br>
            {% endfor %}
        </div>

        <div>
            {{ form.index.label }}<br>
            {{ form.index(size=40) }}<br>
            {% for error in form.index.errors %}
                <span class="error">{{ error }}</span><br>
            {% endfor %}
        </div>

        <div>
            {{ form.comment.label }}<br>
            {{ form.comment(rows=3, cols=40) }}<br>
            {% for error in form.comment.errors %}
                <span class="error">{{ error }}</span><br>
            {% endfor %}
        </div>

        <button type="submit">Зарегистрироваться</button>
    </form>
</body>
</html>
'''


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        return f'''
        <h1>Регистрация успешна!</h1>
        <p>Email: {form.email.data}</p>
        <p>Телефон: {form.phone.data}</p>
        <p>Имя: {form.name.data}</p>
        <p>Адрес: {form.address.data}</p>
        <p>Индекс: {form.index.data}</p>
        <p>Комментарий: {form.comment.data or 'Нет'}</p>
        <a href="/registration">Назад</a>
        '''

    return render_template_string(HTML_FORM, form=form)


# ========== Задача 4: Время работы системы ==========
@app.route('/uptime')
def uptime():
    """Возвращает время работы системы"""
    try:
        result = subprocess.run(['uptime', '-p'], capture_output=True, text=True)
        uptime_str = result.stdout.strip()
        return f"Current uptime is {uptime_str}"
    except Exception as e:
        return f"Ошибка: {str(e)}"


# ========== Задача 5: Текущие процессы ==========
@app.route('/ps')
def ps_command():
    """Выполняет команду ps с переданными аргументами"""
    args = request.args.getlist('arg')

    if not args:
        return '<pre>Не передано ни одного аргумента. Пример: /ps?arg=a&arg=u&arg=x</pre>'

    try:
        command_parts = ['ps']
        for arg in args:
            command_parts.append(shlex.quote(arg))

        command_str = ' '.join(command_parts)
        command = shlex.split(command_str)

        result = subprocess.run(command, capture_output=True, text=True)

        output = result.stdout if result.stdout else result.stderr

        return f'<pre>{output}</pre>'

    except Exception as e:
        return f'<pre>Ошибка: {str(e)}</pre>'


if __name__ == '__main__':
    app.run(debug=True)