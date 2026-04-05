import unittest
import sys
from io import StringIO
from redirect import Redirect


class TestRedirect(unittest.TestCase):

    def test_redirect_stdout(self):

        stdout_capture = StringIO()

        with Redirect(stdout=stdout_capture):
            print('Inside redirect')

        self.assertEqual(stdout_capture.getvalue().strip(), 'Inside redirect')

    def test_redirect_stderr(self):

        stderr_capture = StringIO()

        with Redirect(stderr=stderr_capture):
            sys.stderr.write('Error message\n')

        self.assertEqual(stderr_capture.getvalue().strip(), 'Error message')

    def test_redirect_both_streams(self):

        stdout_capture = StringIO()
        stderr_capture = StringIO()

        with Redirect(stdout=stdout_capture, stderr=stderr_capture):
            print('Stdout text')
            sys.stderr.write('Stderr text\n')

        self.assertEqual(stdout_capture.getvalue().strip(), 'Stdout text')
        self.assertEqual(stderr_capture.getvalue().strip(), 'Stderr text')

    def test_restore_after_exception(self):

        stdout_capture = StringIO()
        original_stdout = sys.stdout

        try:
            with Redirect(stdout=stdout_capture):
                print('Inside')
                raise ValueError('Test error')
        except ValueError:
            pass

        self.assertEqual(sys.stdout, original_stdout)

    def test_no_arguments(self):

        with Redirect():
            print('Nothing changes')
        self.assertTrue(True)

    def test_only_stdout_argument(self):

        stdout_capture = StringIO()
        original_stdout = sys.stdout

        with Redirect(stdout=stdout_capture):
            print('Only stdout redirected')

        self.assertEqual(sys.stdout, original_stdout)
        self.assertEqual(stdout_capture.getvalue().strip(), 'Only stdout redirected')

    def test_only_stderr_argument(self):

        stderr_capture = StringIO()
        original_stderr = sys.stderr

        with Redirect(stderr=stderr_capture):
            sys.stderr.write('Only stderr redirected\n')

        self.assertEqual(sys.stderr, original_stderr)
        self.assertEqual(stderr_capture.getvalue().strip(), 'Only stderr redirected')


if __name__ == '__main__':
    unittest.main()