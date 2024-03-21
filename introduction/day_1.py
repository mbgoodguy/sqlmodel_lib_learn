import random
import string
from typing import Optional

from sqlalchemy import create_engine, column
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field, select, Session

engine = create_engine("sqlite:///database.sqlite", echo=True)
session = Session(engine)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(min_length=2, unique=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def generate_usernames(count: int, length: int) -> list:
    usernames = []

    characters = string.ascii_letters + string.digits
    for i in range(1, count + 1):
        username = ''.join(random.choice(characters) for _ in range(1, length + 1))
        usernames.append(username)
    print(usernames)
    return usernames


# print(generate_usernames(10, 6))


def add_users(count: 10, length: 6):
    with session as db:
        usernames = generate_usernames(count=count, length=length)
        for username in usernames:
            db.add(User(username=username))
            # делать коммит после каждого добавления не имеет смысла. Лучше коммитнуть после всех добавлений
        db.commit()


def get_users_containing(num: int):
    with session as db:
        query = select(User).filter(column('username').contains(f'{num}'))
        usernames = session.exec(query).all()
        first_res = session.exec(query).first()
        print(f'First row in result: {first_res}')
        print(f'List of usernames containing {num}: {usernames}')


if __name__ == '__main__':
    create_db_and_tables()
    add_users(count=15, length=4)  # ok
    get_users_containing(2)
