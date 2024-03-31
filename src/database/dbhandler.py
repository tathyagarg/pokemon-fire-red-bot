import pathlib
import sqlite3
from constants import BOT_DATA

DATA = BOT_DATA.DATABASE

DATABASE = pathlib.Path(__file__).parent.joinpath(DATA.DB_FILE)
DATABASE_NAME = DATA.DB_NAME

def check_user_exists(uid: int) -> bool:
    """ Checks if a user exists in the database """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM {} WHERE {} = ?".format(DATABASE_NAME, DATA.USER_ID), (uid,))
        return cursor.fetchone() is not None

def register_user(uid: int):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO {}{} VALUES(?, '')".format(
            DATABASE_NAME,
            f"({','.join(DATA.FIELDS)})"
        ), (uid,))

def run_sql(sql: str, values: tuple = None):
    values = values or ()
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        return cursor.fetchall()
