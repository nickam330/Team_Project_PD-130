from base_information import Base, Users, Selected, UsersSelected
from create_session import engine


def create_table():
    Users.__table__.create(bind=engine, checkfirst=True)
    Selected.__table__.create(bind=engine, checkfirst=True)
    UsersSelected.__table__.create(bind=engine, checkfirst=True)

create_table()
