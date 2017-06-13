#!/usr/bin/env python3
# Importing some sqlachemy stuff we need to set up our database
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
# Creating User, Category, CategoryItem models


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    items = relationship("CategoryItem", back_populates="user")


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    items = relationship("CategoryItem", back_populates="category")

    def dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "item": [i.dict() for i in self.items]
        }


class CategoryItem(Base):
    __tablename__ = "category_item"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String(256))
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="items")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="items")

    def dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "decription": self.description,
            "category_id": self.category_id,
            "user_id": self.user_id
        }
# Creating engine
engine = create_engine("sqlite:///catalog.db")
Base.metadata.create_all(engine)
