from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from models import PurchaseOrder, Vendor
from schemas import (
    PurchaseOrderCreate,
    PurchaseOrderUpdate,
    PurchaseOrderResponse
)
from dependencies import manager_or_admin

router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"]
)


# ==========================
# Create Purchase Order
# ==========================

@router.post("/", response_model=PurchaseOrderResponse)
def create_purchase_order(
    order: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(manager_or_admin)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == order.vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found."
        )

    if not vendor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot create purchase order for an inactive vendor."
        )

    total_amount = order.quantity * order.unit_price

    new_order = PurchaseOrder(
        vendor_id=order.vendor_id,
        product_name=order.product_name,
        quantity=order.quantity,
        unit_price=order.unit_price,
        total_amount=total_amount,
        expected_delivery_date=order.expected_delivery_date,
        status="Pending"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

# ==========================
# Get All Purchase Orders
# Filter + Search + Pagination
# ==========================

@router.get("/", response_model=list[PurchaseOrderResponse])
def get_purchase_orders(
    status: str | None = Query(default=None),
    product_name: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(manager_or_admin)
):

    query = db.query(PurchaseOrder)

    # Filter by Status
    if status:
        query = query.filter(PurchaseOrder.status == status)

    # Search by Product Name
    if product_name:
        query = query.filter(
            PurchaseOrder.product_name.ilike(f"%{product_name}%")
        )

    # Pagination
    offset = (page - 1) * limit

    orders = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return orders

# ==========================
# Get Purchase Order By ID
# ==========================

@router.get("/{order_id}", response_model=PurchaseOrderResponse)
def get_purchase_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(manager_or_admin)
):
    order = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Purchase order not found."
        )

    return order


# ==========================
# Update Purchase Order
# ==========================

@router.put("/{order_id}", response_model=PurchaseOrderResponse)
def update_purchase_order(
    order_id: int,
    order: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(manager_or_admin)
):
    existing_order = db.query(PurchaseOrder).filter(
        PurchaseOrder.id == order_id
    ).first()

    if not existing_order:
        raise HTTPException(
            status_code=404,
            detail="Purchase order not found."
        )

    # Business Rule:
    # Received orders cannot be edited
    if existing_order.status == "Received":
        raise HTTPException(
            status_code=400,
            detail="Received orders cannot be edited."
        )

    total_amount = order.quantity * order.unit_price

    existing_order.product_name = order.product_name
    existing_order.quantity = order.quantity
    existing_order.unit_price = order.unit_price
    existing_order.total_amount = total_amount
    existing_order.expected_delivery_date = order.expected_delivery_date
    existing_order.status = order.status

    db.commit()
    db.refresh(existing_order)

    return existing_order


# ==========================
# Purchase History By Vendor
# ==========================

@router.get("/vendor/{vendor_id}/history", response_model=list[PurchaseOrderResponse])
def purchase_history(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(manager_or_admin)
):
    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found."
        )

    return db.query(PurchaseOrder).filter(
        PurchaseOrder.vendor_id == vendor_id
    ).all()