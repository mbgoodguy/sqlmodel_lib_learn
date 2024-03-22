import random
import string
from typing import Optional

from sqlalchemy import create_engine, column, func
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
    for i in range(2, count + 1):
        username = ''.join(random.choice(characters) for _ in range(random.randint(2, length + 1)))
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


def get_users_where():
    with session as db:
        query = select(User).where(func.upper(User.username) == User.username)
        res = session.exec(query).all()
        print(f'Count of users with username in uppercase: {len(res)}')
        print(res)


def get_users_with_limit(value: int):
    limited_query = select(User).limit(value)
    print(f'Limited query: {limited_query}')
    res = session.exec(limited_query).all()
    print(res)


def get_users_with_limit_and_offset(limit: int, offset: int):
    query = select(User).limit(limit).offset(offset)
    print(f'Limited query: {query}')
    res = session.exec(query).all()
    print(res)


def update_user_by_id(user_id: int):
    with session as db:
        user = db.get(User, user_id)
        user.username = 'Aboba'
        db.commit()
        print(f'User with id {user_id} has been updated')


def delete_user_by_id(user_id: int):
    with session as db:
        user = db.get(User, user_id)
        db.delete(user)
        db.commit()
        print(f'User with id {user_id} has been deleted')


if __name__ == '__main__':
    # create_db_and_tables()
    # add_users(count=15, length=4)  # ok
    # get_users_containing(2)
    # get_users_where()
    # get_users_with_limit(value=6)
    # get_users_with_limit_and_offset(5, 5)
    # update_user_by_id(5)
    delete_user_by_id(2)
