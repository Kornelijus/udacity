#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, CategoryItem

engine = create_engine("sqlite:///catalog.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

fakeusers = [
    User(name="Admin", email="admin@fake.user")
]

categories = [
    Category(name="CPU"),
    Category(name="Motherboard"),
    Category(name="Memory"),
    Category(name="Storage"),
    Category(name="Video Card")
]

items = [
    CategoryItem(name="Intel Core i7-7700K", category_id=1, user_id=1),
    CategoryItem(name="Intel Core i5-7600K", category_id=1, user_id=1),
    CategoryItem(name="AMD Ryzen 5 1600", category_id=1, user_id=1),
    CategoryItem(name="AMD Ryzen 5 1400", category_id=1, user_id=1),

    CategoryItem(name="Asus STRIX Z270-E GAMING", category_id=2, user_id=1),
    CategoryItem(name="Asus Z170 PRO GAMING", category_id=2, user_id=1),
    CategoryItem(name="MSI Z170A GAMING M5", category_id=2, user_id=1),
    CategoryItem(name="MSI B350M GAMING PRO", category_id=2, user_id=1),

    CategoryItem(name="Corsair Vengeance LPX", category_id=3, user_id=1),
    CategoryItem(name="Crucial Ballistix Sport LT", category_id=3, user_id=1),
    CategoryItem(name="G.Skill Ripjaws V Series", category_id=3, user_id=1),
    CategoryItem(name="G.Skill Ripjaws 4 series", category_id=3, user_id=1),

    CategoryItem(name="Western Digital WD10EZEX", category_id=4, user_id=1),
    CategoryItem(name="Samsung MZ-75E250B/AM", category_id=4, user_id=1),
    CategoryItem(name="Samsung MZ-75E500B/AM", category_id=4, user_id=1),
    CategoryItem(name="Seagate ST2000DM006", category_id=4, user_id=1),

    CategoryItem(
        name="MSI GEFORCE GTX 1060 GAMING X 6G",
        category_id=5,
        user_id=1),
    CategoryItem(name="EVGA 04G-P4-6253-KR", category_id=5, user_id=1),
    CategoryItem(
        name="Asus STRIX-GTX1080TI-O11G-GAMING",
        category_id=5,
        user_id=1),
    CategoryItem(name="EVGA 06G-P4-6161-KR", category_id=5, user_id=1)
]
session.add_all(fakeusers)
session.add_all(categories)
session.add_all(items)
try:
    session.commit()
except BaseException:
    print("Failed to commit!\a")
