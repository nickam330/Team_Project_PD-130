import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from sqlalchemy.orm import declarative_base, relationship
from information import*
import os

load_dotenv()

key = os.environ.get('FERNET_KEY')
if not key:
    raise ValueError("FERNET_KEY не найден!")
fernet = Fernet(key.encode())

dsn = os.getenv('DATABASE_URL')

engine = sq.create_engine(dsn)
Session = sessionmaker(bind=engine)
