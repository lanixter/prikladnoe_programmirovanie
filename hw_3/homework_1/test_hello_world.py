import unittest
from freezegun import freeze_time
from app import app


class TestHelloWorld(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @freeze_time("2024-04-01")
    def test_can_get_correct_weekday_monday(self):
        response = self.app.get('/hello-world/Анна')
        self.assertEqual(response.status_code, 200)
        self.assertIn('понедельника', response.data.decode())

    @freeze_time("2024-04-02")
    def test_can_get_correct_weekday_tuesday(self):
        response = self.app.get('/hello-world/Анна')
        self.assertEqual(response.status_code, 200)
        self.assertIn('вторника', response.data.decode())

    @freeze_time("2024-04-03")
    def test_can_get_correct_weekday_wednesday(self):
        response = self.app.get('/hello-world/Анна')
        self.assertEqual(response.status_code, 200)
        self.assertIn('среды', response.data.decode())

    @freeze_time("2024-04-04")
    def test_can_get_correct_weekday_thursday(self):
        response = self.app.get('/hello-world/Анна')
        self.assertEqual(response.status_code, 200)
        self.assertIn('четверга', response.data.decode())

    @freeze_time("2024-04-05")
    def test_can_get_correct_weekday_friday(self):
        response = self.app.get('/hello-world/Анна')
        self.assertEqual(response.status_code, 200)
        self.assertIn('пятницы', response.data.decode())

    @freeze_time("2024-04-06")
    def test_can_get_correct_weekday_saturday(self):
        response = self.app.get('/hello-world/Анна')
        self.assertEqual(response.status_code, 200)
        self.assertIn('субботы', response.data.decode())

    @freeze_time("2024-04-07")
    def test_can_get_correct_weekday_sunday(self):
        response = self.app.get('/hello-world/Анна')
        self.assertEqual(response.status_code, 200)
        self.assertIn('воскресенья', response.data.decode())

    def test_can_get_correct_username(self):
        response = self.app.get('/hello-world/Петр')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Петр', response.data.decode())


if __name__ == '__main__':
    unittest.main()