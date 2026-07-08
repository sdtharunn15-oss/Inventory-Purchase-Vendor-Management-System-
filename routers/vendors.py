from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Vendor
from schemas import VendorCreate, VendorUpdate, VendorResponse
from dependencies import admin_required

router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"]
)


# ==========================
# Create Vendor
# ==========================

@router.post("/", response_model=VendorResponse)
def create_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    existing_vendor = db.query(Vendor).filter(
        Vendor.email == vendor.email
    ).first()

    if existing_vendor:
        raise HTTPException(
            status_code=400,
            detail="Vendor email already exists."
        )

    new_vendor = Vendor(
        vendor_name=vendor.vendor_name,
        email=vendor.email,
        phone=vendor.phone,
        address=vendor.address,
        is_active=True
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)

    return new_vendor


# ==========================
# Get All Vendors
# ==========================

@router.get("/", response_model=list[VendorResponse])
def get_vendors(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return db.query(Vendor).all()


# ==========================
# Get Vendor By ID
# ==========================

@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found."
        )

    return vendor


# ==========================
# Update Vendor
# ==========================

@router.put("/{vendor_id}", response_model=VendorResponse)
def update_vendor(
    vendor_id: int,
    vendor: VendorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    existing_vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not existing_vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found."
        )

    email_exists = db.query(Vendor).filter(
        Vendor.email == vendor.email,
        Vendor.id != vendor_id
    ).first()

    if email_exists:
        raise HTTPException(
            status_code=400,
            detail="Vendor email already exists."
        )

    existing_vendor.vendor_name = vendor.vendor_name
    existing_vendor.email = vendor.email
    existing_vendor.phone = vendor.phone
    existing_vendor.address = vendor.address
    existing_vendor.is_active = vendor.is_active

    db.commit()
    db.refresh(existing_vendor)

    return existing_vendor


# ==========================
# Soft Delete Vendor
# ==========================

@router.delete("/{vendor_id}")
def delete_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found."
        )

    vendor.is_active = False

    db.commit()

    return {
        "message": "Vendor deactivated successfully."
    }