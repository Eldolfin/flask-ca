from __future__ import annotations
from enum import StrEnum
from flask_login import UserMixin


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


class Todo:
    tag: Tag
    degree: Degree
    content: str
    userid: str

    def __init__(self, tag: str, degree: str, content: str, userid: str) -> None:
        self.tag = Tag(tag)
        self.degree = Degree(degree)
        self.content = content
        self.userid = userid

    def __iter__(self):
        yield 'tag', self.tag
        yield 'degree', self.degree
        yield 'content', self.content
        yield 'userid', self.userid

    @classmethod
    def fromdict(cls, d: dict[str, str]) -> Todo:
        return cls(Tag(d['tag']), Degree(d['degree']), d['content'], d['userid'])
