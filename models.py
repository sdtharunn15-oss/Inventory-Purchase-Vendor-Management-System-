from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    purchase_orders = relationship(
        "PurchaseOrder",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    expected_delivery_date = Column(Date, nullable=False)
    status = Column(String, default="Pending")

    vendor = relationship(
        "Vendor",
        back_populates="purchase_orders"
    )