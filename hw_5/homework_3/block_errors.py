from types import TracebackType
from typing import Type, Optional, Set, Union


class BlockErrors:


    def __init__(self, errors: Union[Type[Exception], Set[Type[Exception]]]):

        if isinstance(errors, type):
            self.errors = {errors}
        else:
            self.errors = set(errors)

    def __enter__(self):
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> bool:

        if exc_type is None:
            return False


        for error_type in self.errors:
            if issubclass(exc_type, error_type):
                return True

        return False