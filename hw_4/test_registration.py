import unittest
from app import app


class TestRegistration(unittest.TestCase):

    def setUp(self):
        # Отключаем CSRF для тестов
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app.testing = True

    def test_email_valid(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Регистрация успешна'.encode(), response.data)

    def test_email_invalid(self):
        response = self.app.post('/registration', data={
            'email': 'invalid-email',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Введите корректный email'.encode(), response.data)

    def test_email_empty(self):
        response = self.app.post('/registration', data={
            'email': '',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Email обязателен для заполнения'.encode(), response.data)

    def test_phone_valid(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Регистрация успешна'.encode(), response.data)

    def test_phone_invalid_length(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '12345',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Телефон должен содержать ровно 10 цифр'.encode(), response.data)

    def test_phone_not_digits(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '12345678a0',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Телефон должен содержать только цифры'.encode(), response.data)

    def test_phone_empty(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Телефон обязателен для заполнения'.encode(), response.data)

    def test_name_valid(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Регистрация успешна'.encode(), response.data)

    def test_name_empty(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': '',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Имя обязательно для заполнения'.encode(), response.data)

    def test_address_valid(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Регистрация успешна'.encode(), response.data)

    def test_address_empty(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': '',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Адрес обязателен для заполнения'.encode(), response.data)

    def test_index_valid(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Тест'
        })
        self.assertIn('Регистрация успешна'.encode(), response.data)

    def test_index_not_digits(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '12a456',
            'comment': 'Тест'
        })
        self.assertIn('Индекс должен содержать только цифры'.encode(), response.data)

    def test_index_empty(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '',
            'comment': 'Тест'
        })
        self.assertIn('Индекс обязателен для заполнения'.encode(), response.data)

    def test_comment_empty_valid(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': ''
        })
        self.assertIn('Регистрация успешна'.encode(), response.data)


if __name__ == '__main__':
    unittest.main()