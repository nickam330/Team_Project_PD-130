from base_information import *
from create_session import engine


def drop_table():
    Base.metadata.drop_all(engine)

drop_table()