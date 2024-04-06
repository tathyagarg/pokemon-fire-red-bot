import toml
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

class Database:
    def __init__(self, **kwargs) -> None:
        self.DB_FILE: str = kwargs['DB_FILE']

        self.DB_NAME: str = kwargs['DB_NAME']
        self.USER_ID: str = kwargs['UID']
        self.PARTY: str = kwargs['PARTY']
        self.USE_NAME: str = kwargs['USE_NAME']

        self.FIELDS: list[str] = [self.USER_ID, self.PARTY, self.USE_NAME]

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
    