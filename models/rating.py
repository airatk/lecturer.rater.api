from peewee import AutoField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField

from models.base import Base
from models.user import User


class Rating(Base):
    id: AutoField = AutoField()

    user_id: ForeignKeyField = ForeignKeyField(model=User, index=True, on_delete="CASCADE")

    lecturer: TextField = TextField()
    value: IntegerField = IntegerField()
    text: TextField = TextField(default="")
