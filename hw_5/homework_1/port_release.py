import os
import signal
import subprocess
import time
from flask import Flask

app = Flask(__name__)


def find_process_by_port(port):

    try:
        result = subprocess.run(
            ['lsof', '-i', f':{port}', '-t'],
            capture_output=True,
            text=True
        )
        pids = result.stdout.strip().split('\n')
        return [int(pid) for pid in pids if pid]
    except Exception:
        return []


def kill_process(pid):

    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        return True
    except Exception:
        return False


def free_port(port):

    pids = find_process_by_port(port)
    for pid in pids:
        kill_process(pid)
    return len(pids) > 0


def run_server_with_port_release(port, app):

    free_port(port)
    app.run(port=port, debug=False)


@app.route('/')
def index():
    return 'Server is running!'


if __name__ == '__main__':
    run_server_with_port_release(5000, app)