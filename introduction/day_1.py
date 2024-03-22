import random
import string
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine, column, func
from sqlmodel import SQLModel, Field, select, Session

db_dir_path = Path(__file__).parent.parent / 'databases'
sqlite_file_name = "day_1.sqlite"
sqlite_url = f"sqlite:///{db_dir_path}/{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)
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

def check_user_exist(db: session, user_id: int):
    user = db.get(User, user_id)
    if user is not None:
        print(f'User with id {user_id} exists')
        return user
    return None


def print_no_user_with(user_id: int):
    print(f'No user with id {user_id}')


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


def get_users_w_full_uppercase():
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
        user = check_user_exist(db=db, user_id=user_id)
        if user:
            user.username = 'Aboba'
            db.commit()
            print(f'User with id {user_id} has been updated')
        else:
            print_no_user_with(user_id)


def delete_user_by_id(user_id: int):
    with session as db:
        user = check_user_exist(db=db, user_id=user_id)
        if user is not None:
            db.delete(user)
            db.commit()
            print(f'User with id {user_id} has been deleted')
        else:
            print_no_user_with(user_id)


if __name__ == '__main__':
    # create_db_and_tables()
    # add_users(count=15, length=4)  # ok
    # check_user_exist(db=session, user_id=1)
    # get_users_containing(2)
    # get_users_w_full_uppercase()
    # get_users_with_limit(value=6)
    # get_users_with_limit_and_offset(5, 5)
    # update_user_by_id(5)
    delete_user_by_id(1)
