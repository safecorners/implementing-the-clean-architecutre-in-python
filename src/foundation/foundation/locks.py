from types import TracebackType
from typing import Callable, Literal, Optional, Protocol, Type


class AlreadyLocked(Exception):
    ...


class Lock(Protocol):
    def __enter__(self) -> None:
        ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        ...


LockFactory = Callable[[str, int], Lock]
