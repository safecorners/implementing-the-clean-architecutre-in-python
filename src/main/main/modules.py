import threading
from typing import Type

import injector
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import Session


# https://injector.readthedocs.io/en/latest/scopes.html#implementing-new-scopes
class RequestScope(injector.Scope):
    REGISTRY_KEY = "RequestScopeRegistry"

    def configure(self) -> None:
        self._locals = threading.local()

    def enter(self) -> None:
        assert not hasattr(self._locals, self.REGISTRY_KEY)
        setattr(self._locals, self.REGISTRY_KEY, {})

    def exit(self) -> None:
        for key, provider in getattr(self._locals, self.REGISTRY_KEY).items():
            provider.get(self.injector).close()
            delattr(self._locals, repr(key))

        delattr(self._locals, self.REGISTRY_KEY)

    def __enter__(self) -> None:
        self.enter()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.exit()

    def get(
        self, key: Type[injector.T], provider: injector.Provider[injector.T]
    ) -> injector.Provider[injector.T]:
        try:
            return getattr(self._locals, repr(key))
        except AttributeError:
            provider = injector.InstanceProvider(provider.get(self.injector))
            setattr(self._locals, repr(key), provider)
            try:
                registry = getattr(self._locals, self.REGISTRY_KEY)
            except AttributeError:
                raise Exception(
                    f"{key} is request scoped, but no RequestScope entered!"
                )
            registry[key] = provider
            return provider


request = injector.ScopeDecorator(RequestScope)


class Db(injector.Module):
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    @request
    @injector.provider
    def connection(self) -> Connection:
        return self._engine.connect()

    @request
    @injector.provider
    def session(self, connection: Connection) -> Session:
        return Session(bind=connection)
