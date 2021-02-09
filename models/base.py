from peewee import PostgresqlDatabase
from peewee import Model


class Base(Model):
    class Meta:
        database: PostgresqlDatabase = PostgresqlDatabase(database="lecturer_rater_db")
        legacy_table_names: bool = False
