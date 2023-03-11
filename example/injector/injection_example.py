from typing import NewType

from injector import Binder, Injector, Module, inject, provider

Name = NewType("Name", str)
Description = NewType("Description", str)


class User:
    @inject
    def __init__(self, name: Name, description: Description) -> None:
        self.name = name
        self.description = description


class UserModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(User)


class UserAttributeModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(Name, to=Name("Sherlock"))

    @provider
    def describe(self, name: Name) -> Description:
        return Description("%s is a man of astounding insight" % name)


class NumberModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(int, to=654)

    @provider
    def provider_str(self, i: int) -> str:
        return str(i)


injector = Injector([UserModule(), UserAttributeModule()])

user = injector.get(User)
print(f"{injector.get(Name)} - {injector.get(Description)}")
print(f"{user.name} - {user.description}")
