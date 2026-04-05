import unittest
from block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):

    def test_ignore_specific_error(self):

        err_types = {ZeroDivisionError}
        with BlockErrors(err_types):
            a = 1 / 0
        self.assertTrue(True)

    def test_propagate_unexpected_error(self):

        err_types = {ZeroDivisionError}
        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 / '0'

    def test_nested_blocks(self):

        outer_err_types = {TypeError}
        result = []

        with BlockErrors(outer_err_types):
            inner_err_types = {ZeroDivisionError}
            with BlockErrors(inner_err_types):
                a = 1 / '0'
            result.append('inner')

        result.append('outer')
        self.assertEqual(result, ['outer'])

    def test_ignore_base_exception(self):

        err_types = {Exception}
        with BlockErrors(err_types):
            a = 1 / '0'
        self.assertTrue(True)

    def test_ignore_child_exception(self):

        err_types = {ZeroDivisionError}
        with BlockErrors(err_types):
            a = 1 / 0
        self.assertTrue(True)

    def test_ignore_multiple_error_types(self):

        err_types = {ZeroDivisionError, TypeError}
        with BlockErrors(err_types):
            a = 1 / '0'
        self.assertTrue(True)

    def test_single_error_type_as_argument(self):

        with BlockErrors(ZeroDivisionError):
            a = 1 / 0
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()