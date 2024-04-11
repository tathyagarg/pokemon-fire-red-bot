import json
import typing
import pathlib
import constants
from global_vars import *
import entities.data as data
from constants import BOT_DATA

DATA: constants.Database = BOT_DATA.DATABASE

DATABASE: pathlib.PosixPath = pathlib.Path(__file__).parent.joinpath(DATA.DB_FILE)

def dump(data, fp):
    json.dump(data, fp, indent=4)

def check_user_exists(uid: int) -> bool:
    """ Checks if a user exists in the database """
    with open(DATABASE) as f:
        data = json.load(f)
        return data.get(str(uid)) is not None

def register_user(uid: int) -> None:
    with open(DATABASE) as f:
        data = json.load(f)
    data[str(uid)] = BOT_DATA.DATABASE.EMPTY_USER
    with open(DATABASE, 'w') as f:
        dump(data, f)

def request_data(uid: int) -> dict:
    with open(DATABASE) as f:
        data = json.load(f)
    return data[str(uid)]

def dump_user_data(uid: int, data: dict) -> None:
    with open(DATABASE) as f:
        original = json.load(f)
    original[str(uid)] = data
    with open(DATABASE, 'w') as f:
        dump(original, f)

def request_field(uid: int, field: str) -> typing.Any:
    with open(DATABASE) as f:
        data = json.load(f)
    return data[str(uid)][field]

def update_field(uid: int, field: str, new_value) -> None:
    original = request_data(uid=uid)
    original[field] = new_value
    dump_user_data(uid=uid, data=original)

def fetch_player_intro_sprite(uid: int):
    """
        :return: Character object representing the player's chosen gender
    """
    is_male: bool = request_field(uid=uid, field=DATA.IS_MALE)
    return data.RED if is_male else data.LEAF
