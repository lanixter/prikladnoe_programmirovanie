import unittest
from app import app, storage


class TestFinance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def setUp(self):
        storage.clear()

    def test_add_expense_valid_date(self):
        response = self.app.get('/add/20240315/500')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Добавлена трата 500 руб. за 15.3.2024', response.data.decode())

    def test_add_multiple_expenses_same_day(self):
        self.app.get('/add/20240315/500')
        self.app.get('/add/20240315/300')
        response = self.app.get('/calculate/2024/3')
        self.assertIn('800', response.data.decode())

    def test_add_expenses_different_months(self):
        self.app.get('/add/20240315/500')
        self.app.get('/add/20240415/1000')
        response_march = self.app.get('/calculate/2024/3')
        response_april = self.app.get('/calculate/2024/4')
        self.assertIn('500', response_march.data.decode())
        self.assertIn('1000', response_april.data.decode())

    def test_calculate_year_total(self):
        self.app.get('/add/20240315/500')
        self.app.get('/add/20240415/1000')
        self.app.get('/add/20240515/700')
        response = self.app.get('/calculate/2024')
        self.assertIn('2200', response.data.decode())

    def test_calculate_month_total(self):
        self.app.get('/add/20240315/500')
        self.app.get('/add/20240320/300')
        self.app.get('/add/20240325/200')
        response = self.app.get('/calculate/2024/3')
        self.assertIn('1000', response.data.decode())

    def test_calculate_year_no_data(self):
        response = self.app.get('/calculate/2023')
        self.assertIn('не найдено', response.data.decode())

    def test_calculate_month_no_data(self):
        response = self.app.get('/calculate/2024/6')
        self.assertIn('не найдено', response.data.decode())


if __name__ == '__main__':
    unittest.main()