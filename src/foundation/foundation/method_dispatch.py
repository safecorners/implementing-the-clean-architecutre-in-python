import functools
from typing import Any, Callable


def method_dispatch(func: Callable[..., Any]) -> Callable[..., Any]:
    dispatcher = functools.singledispatch(func)

    def wrapper(*args, **kwargs):
        return dispatcher.dispatch(args[1].__class__)(*args, **kwargs)

    wrapper.register = dispatcher.register
    wrapper.registry = dispatcher.registry
    functools.update_wrapper(wrapper, func)
    return wrapper
