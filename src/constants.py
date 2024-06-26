import toml
import typing
import pathlib

parent: pathlib.PosixPath = pathlib.Path(__file__).parents[1]  # parent directory of src
config: pathlib.PosixPath = parent.joinpath('config.toml')

class BotData:
    """
        Implementing this class so that IDE can help prevent me typoing constant names
    """
    def __init__(self, **kwargs) -> None:
        self.TOKEN: str = kwargs.get("TOKEN")
        self.GUILD_IDS: list[int] = kwargs.get('GUILD_IDS', [])
        self.COLORS: Colors = kwargs.get('COLORS')
        self.DATABASE: Database = kwargs.get('DATABASE')
        self.UNITS: int = 48

class Database:
    def __init__(self, **kwargs) -> None:
        self.DB_FILE: str = kwargs['DB_FILE']

        self.PARTY = 'party'
        self.USERNAME = 'username'
        self.OPPONENT = 'opponent'
        self.PROGRESSION = 'location'
        self.POSITION_X = 'position_x'
        self.POSITION_Y = 'position_y'
        self.POSITION = 'position'
        self.IS_MALE = 'gender'
        self.DIRECTION = 'direction'

        self.EMPTY_USER: dict[str, typing.Any] = {
            self.PARTY: [],
            self.USERNAME: '',
            self.OPPONENT: '',
            self.PROGRESSION: -1,
            self.POSITION_X: -1,
            self.POSITION_Y: -1,
            self.IS_MALE: -1,
            self.DIRECTION: 0
        }

        self.FIELDS = [self.PARTY, self.USERNAME, self.PROGRESSION, self.POSITION_X, self.POSITION_Y, self.IS_MALE]

class Colors:
    def __init__(self, **kwargs) -> None:
        self.COLOR_PRIMARY: int = kwargs['COLOR_PRIMARY']
        self.COLOR_SECONDARY: int = kwargs['COLOR_SECONDARY']
        self.COLOR_ERROR: int = kwargs['COLOR_ERROR']
        self.COLOR_SUCCESS: int = kwargs['COLOR_SUCCESS']
        self.COLOR_INFO: int = kwargs['COLOR_INFO']

with open(file=config, mode='r') as f:
    data: dict[str, str | dict[str, str | int]] = toml.load(f)

    BOT_DATA: BotData = BotData(**data)
    BOT_DATA.DATABASE = Database(**data['DATABASE'])
    BOT_DATA.COLORS = Colors(**data['COLORS'])
    