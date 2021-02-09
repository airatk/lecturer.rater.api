from models.user import User
from models.rating import Rating


def setup_database_tables():
    User.create_table()
    Rating.create_table()
