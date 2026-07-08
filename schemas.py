from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================
# User Schemas
# ==========================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["Admin", "Store Manager"]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


# ==========================
# Vendor Schemas
# ==========================

class VendorCreate(BaseModel):
    vendor_name: str
    email: EmailStr
    phone: str
    address: str


class VendorUpdate(BaseModel):
    vendor_name: str
    email: EmailStr
    phone: str
    address: str
    is_active: bool


class VendorResponse(BaseModel):
    id: int
    vendor_name: str
    email: EmailStr
    phone: str
    address: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ==========================
# Purchase Order Schemas
# ==========================

class PurchaseOrderCreate(BaseModel):
    vendor_id: int
    product_name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    expected_delivery_date: date


class PurchaseOrderUpdate(BaseModel):
    product_name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    expected_delivery_date: date
    status: Literal["Pending", "Approved", "Received", "Cancelled"]


class PurchaseOrderResponse(BaseModel):
    id: int
    vendor_id: int
    product_name: str
    quantity: int
    unit_price: float
    total_amount: float
    expected_delivery_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)