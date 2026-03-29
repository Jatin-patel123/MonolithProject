from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# ---------------- USERS ----------------
class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    password = Column(String(255))
    role = Column(String(10))


# ---------------- PRODUCTS ----------------
class Product(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    buying_price = Column(Float)
    selling_price = Column(Float)
    quantity = Column(Integer)
    qty_alert = Column(Integer)


# ---------------- BILL ITEMS ----------------
class BillItem(Base):
    __tablename__ = "BillItems"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


# ---------------- RETURNS ----------------
class Return(Base):
    __tablename__ = "Returns"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    quantity = Column(Integer)
    refund_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)