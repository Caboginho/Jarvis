import os
from sqlalchemy import (
    create_engine, Column, Integer, String, Float,
    Text, ForeignKey, DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime



Base = declarative_base()

# -------------------- User --------------------
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    orders = relationship("Order", back_populates="user")

# -------------------- Product --------------------
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)

    orders = relationship("Order", back_populates="product")

    @staticmethod
    def get_all():
        session = DBSession()
        return session.query(Product).all()

    @staticmethod
    def create(data):
        session = DBSession()
        prod = Product(**data)
        session.add(prod)
        session.commit()
        return prod

# -------------------- Order --------------------
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")

# -------------------- DB Engine / Session --------------------
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
DBSession = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
