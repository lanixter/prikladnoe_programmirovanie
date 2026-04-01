import unittest
import datetime
from person import Person


class TestPerson(unittest.TestCase):

    def setUp(self):
        self.person = Person("Иван", 1990, "Москва, ул. Ленина, д. 1")

    def test_init_with_all_params(self):
        person = Person("Петр", 1995, "СПб, Невский пр., д. 10")
        self.assertEqual(person.name, "Петр")
        self.assertEqual(person.yob, 1995)
        self.assertEqual(person.address, "СПб, Невский пр., д. 10")

    def test_init_without_address(self):
        person = Person("Анна", 2000)
        self.assertEqual(person.name, "Анна")
        self.assertEqual(person.yob, 2000)
        self.assertEqual(person.address, "")

    def test_get_age(self):
        current_year = datetime.datetime.now().year
        expected_age = current_year - 1990
        self.assertEqual(self.person.get_age(), expected_age)

    def test_get_name(self):
        self.assertEqual(self.person.get_name(), "Иван")

    def test_set_name(self):
        self.person.set_name("Алексей")
        self.assertEqual(self.person.get_name(), "Алексей")

    def test_set_address(self):
        self.person.set_address("Казань, ул. Баумана, д. 5")
        self.assertEqual(self.person.get_address(), "Казань, ул. Баумана, д. 5")

    def test_get_address(self):
        self.assertEqual(self.person.get_address(), "Москва, ул. Ленина, д. 1")

    def test_is_homeless_with_address(self):
        self.assertFalse(self.person.is_homeless())

    def test_is_homeless_without_address(self):
        person = Person("Бомж", 1980)
        self.assertTrue(person.is_homeless())

    def test_is_homeless_empty_string(self):
        person = Person("Тест", 2000, "")
        self.assertTrue(person.is_homeless())


if __name__ == '__main__':
    unittest.main()