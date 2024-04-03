from database import run_sql
from constants import BOT_DATA

def check_registered(ctx):
    result = run_sql("SELECT * FROM {} WHERE {} = ?".format(BOT_DATA.DATABASE.DB_NAME, BOT_DATA.DATABASE.USER_ID), (ctx.author.id,))
    return result != []

def check_registered_without_context(user):
    result = run_sql("SELECT * FROM {} WHERE {} = ?".format(BOT_DATA.DATABASE.DB_NAME, BOT_DATA.DATABASE.USER_ID), (user.id,))
    return result != []
