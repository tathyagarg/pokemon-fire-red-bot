import pathlib
import toml

parent = pathlib.Path(__file__).parents[1]  # parent directory of src
config = parent.joinpath('config.toml')

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
        self.DB_FILE = kwargs['DB_FILE']

        self.DB_NAME = kwargs['DB_NAME']
        self.USER_ID = kwargs['UID']
        self.PARTY = kwargs['PARTY']
        self.USE_NAME = kwargs['USE_NAME']

        self.FIELDS = [self.USER_ID, self.PARTY, self.USE_NAME]

class Colors:
    def __init__(self, **kwargs) -> None:
        self.COLOR_PRIMARY = kwargs['COLOR_PRIMARY']
        self.COLOR_ERROR = kwargs['COLOR_ERROR']
        self.COLOR_SUCCESS = kwargs['COLOR_SUCCESS']

with open(config, 'r') as f:
    data = toml.load(f)
    BOT_DATA = BotData(**data)
    BOT_DATA.DATABASE = Database(**data['DATABASE'])
    BOT_DATA.COLORS = Colors(**data['COLORS'])