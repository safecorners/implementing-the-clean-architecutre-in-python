import abc
from typing import Callable, List, Type


class Event:
    ...


class EventMixin:
    def __init__(self) -> None:
        self._pending_domain_events: List[Event] = []

    def _record_event(self, event: Event) -> None:
        self._pending_domain_events.append(event)

    @property
    def domain_events(self) -> List[Event]:
        return self._pending_domain_events[:]

    def clear_events(self) -> None:
        self._pending_domain_events.clear()


class EventBus(abc.ABC):
    @abc.abstractmethod
    def emit(self, event: Event) -> None:
        NotImplementedError

    @abc.abstractmethod
    def subscribe(
        self,
        event_cls: Type[Event],
        listener: Callable,
    ) -> None:
        NotImplementedError
