import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from information import*

dsn = f'postgresql://{login_postgres}:{password_postgres}@localhost:{port}/{basadate_name}'

engine = sq.create_engine(dsn)
Session = sessionmaker(bind=engine)
