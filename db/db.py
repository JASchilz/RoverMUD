from peewee import Model
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('my_database.db')


class BaseModel(Model):
    class Meta:
        database = db


