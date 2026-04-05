import unittest
import subprocess
import time
from port_release import find_process_by_port, kill_process, free_port


class TestPortRelease(unittest.TestCase):

    def setUp(self):

        pass

    def tearDown(self):

        pass

    def test_find_process_by_port_returns_list(self):

        pids = find_process_by_port(5000)
        self.assertIsInstance(pids, list)

    def test_kill_process_terminates_process(self):

        process = subprocess.Popen(['sleep', '10'])
        pid = process.pid
        time.sleep(0.5)
        result = kill_process(pid)
        self.assertTrue(result)

    def test_free_port_releases_port(self):

        process = subprocess.Popen(['python3', '-m', 'http.server', '5000'])
        time.sleep(1)
        result = free_port(5000)
        self.assertTrue(result)
        process.kill()


if __name__ == '__main__':
    unittest.main()