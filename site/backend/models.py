import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    price = Column(Float)

    @staticmethod
    def get_all():
        session = DBSession()
        return session.query(Product).all()

    @staticmethod
    def create(data):
        session = DBSession()
        prod = Product(**data)
        session.add(prod); session.commit()
        return prod

# engine
MYSQL_USER = os.getenv('DB_USER', 'root')
MYSQL_PASS = os.getenv('DB_PASS', '')
MYSQL_HOST = os.getenv('DB_HOST', 'localhost')
MYSQL_DB   = os.getenv('DB_NAME', 'jarvis')
engine = create_engine(
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}/{MYSQL_DB}',
    echo=True
)

#engine = create_engine('sqlite:///site.db', connect_args={'check_same_thread': False})
DBSession = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)