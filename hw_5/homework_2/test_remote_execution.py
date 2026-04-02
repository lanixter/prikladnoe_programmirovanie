import unittest
from remote_execution import execute_code_safely


class TestRemoteExecution(unittest.TestCase):

    def test_simple_code_execution(self):

        result = execute_code_safely('print("Hello World")', 5)
        self.assertTrue(result['success'])
        self.assertIn('Hello World', result['stdout'])

    def test_timeout_exceeded(self):

        result = execute_code_safely('import time; time.sleep(10)', 2)
        self.assertFalse(result['success'])
        self.assertIn('timed out', result['error'])

    def test_syntax_error_handling(self):

        result = execute_code_safely('print("unclosed string)', 5)
        self.assertTrue(result['success'])
        self.assertIn('SyntaxError', result['stderr'])

    def test_resource_limitation(self):

        result = execute_code_safely(
            'import subprocess; subprocess.run(["echo", "hack"])',
            5
        )

        is_blocked = (not result['success'] or
                      'BlockingIOError' in result['stderr'] or
                      'Resource temporarily unavailable' in result['stderr'] or
                      result['returncode'] != 0)
        self.assertTrue(is_blocked, f"Resource limitation failed: {result}")


if __name__ == '__main__':
    unittest.main()