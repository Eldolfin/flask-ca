from __future__ import annotations
from enum import StrEnum
from flask_login import UserMixin
from dataclasses import dataclass, asdict


class User(UserMixin):
    id: str
    email: str
    password: str
    name: str

    def __init__(self, id: str, email: str, password: str, name: str) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.name = name

    # allows conversion from dictionary type
    @classmethod
    def fromdict(cls, d: dict[str, str]) -> User:
        return cls(d['id'], d['email'], d['password'], d['name'])

    # allows conversion to dictionary type
    def __iter__(self):
        yield 'id', self.id
        yield 'email', self.email
        yield 'password', self.password
        yield 'name', self.name


class Tag(StrEnum):
    WORK = "Work",
    PERSONAL = "Personal"


class Degree(StrEnum):
    IMPORTANT = "Important",
    UNIMPORTANT = "Unimportant"


# NamedTuple permits automatic conversion from and to dict
# but was not used for the User model as it doesn't allow
# multiple inheritance
@dataclass
class Todo:
    tag: Tag
    degree: Degree
    content: str

    def __init__(self, tag: str, degree: str, content: str) -> None:
        self.tag = Tag(tag)
        self.degree = Degree(degree)
        self.content = content

    def __iter__(self):
        for k, v in asdict(self).items():
            yield k, str(v)
