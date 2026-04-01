import unittest
from decrypt import decrypt


class TestDecrypt(unittest.TestCase):

    def test_decrypt_with_single_dot(self):
        test_cases = [
            ('абра-кадабра.', 'абра-кадабра'),
            ('1..2.3', '23'),
            ('абр......a.', 'a'),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                result = decrypt(encrypted)
                self.assertEqual(result, expected)

    def test_decrypt_with_double_dot(self):
        test_cases = [
            ('абраа..-кадабра', 'абра-кадабра'),
            ('абраа..-.кадабра', 'абра-кадабра'),
            ('абра--..кадабра', 'абра-кадабра'),
            ('абрау...-кадабра', 'абра-кадабра'),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                result = decrypt(encrypted)
                self.assertEqual(result, expected)

    def test_decrypt_with_multiple_dots(self):
        test_cases = [
            ('абра........', ''),
            ('1.......................', ''),
            ('.', ''),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                result = decrypt(encrypted)
                self.assertEqual(result, expected)

    def test_decrypt_edge_cases(self):
        test_cases = [
            ('', ''),
            ('...', ''),
            ('a..b', 'b'),
            ('ab..', 'a'),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                result = decrypt(encrypted)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()