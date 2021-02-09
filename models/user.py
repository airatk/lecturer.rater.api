from peewee import AutoField
from peewee import TextField

from models.base import Base


class User(Base):
    id: AutoField = AutoField()

    username: TextField = TextField()
    password: TextField = TextField()

    token: TextField = TextField()
