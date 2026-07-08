from fastapi import FastAPI

from database import Base, engine
from routers import auth, vendors, purchase_orders

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Purchase & Vendor Management System",
    version="1.0.0"
)

# Include Routers
app.include_router(auth.router)
app.include_router(vendors.router)
app.include_router(purchase_orders.router)


@app.get("/")
def root():
    return {
        "message": "Inventory Purchase & Vendor Management System API is running successfully!"
    }