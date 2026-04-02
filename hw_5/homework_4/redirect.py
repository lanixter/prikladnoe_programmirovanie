import sys
from io import IOBase
from typing import Optional


class Redirect:
    

    def __init__(
            self,
            stdout: Optional[IOBase] = None,
            stderr: Optional[IOBase] = None
    ):

        self.stdout = stdout
        self.stderr = stderr
        self.old_stdout = None
        self.old_stderr = None

    def __enter__(self):

        if self.stdout is not None:
            self.old_stdout = sys.stdout
            sys.stdout = self.stdout

        if self.stderr is not None:
            self.old_stderr = sys.stderr
            sys.stderr = self.stderr

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self.old_stdout is not None:
            sys.stdout = self.old_stdout

        if self.old_stderr is not None:
            sys.stderr = self.old_stderr


        return False