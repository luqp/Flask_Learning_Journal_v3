import datetime
from peewee import *


DATABASE = SqliteDatabase('journals.db')


class Journal(Model):
    date = DateField(default=datetime.date.today)
    title = CharField()
    learned = TextField()
    resources = TextField()
    time_spent = IntegerField()

    class Meta():
        database = DATABASE
        order_by = ('-date',)

    @classmethod
    def create_journal(cls, date, title, learned, resources, time_spent):
        try:
            with DATABASE.transaction():
                cls.create(
                    date=date,
                    title=title,
                    learned=learned,
                    resources=resources,
                    time_spent=time_spent
                )
        except IntegrityError:
            raise ValueError("")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Journal], safe=True)
    DATABASE.close()
