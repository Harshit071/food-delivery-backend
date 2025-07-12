from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    orders = relationship('Order', back_populates='user')

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    food_items = relationship('FoodItem', back_populates='restaurant')

class FoodItem(Base):
    __tablename__ = 'food_items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship('Restaurant', back_populates='food_items')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    food_item_id = Column(Integer, ForeignKey('food_items.id'))
    quantity = Column(Integer, nullable=False)
    order_time = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='orders')
    food_item = relationship('FoodItem') 