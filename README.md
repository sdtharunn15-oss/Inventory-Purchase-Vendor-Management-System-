Inventory Purchase & Vendor Management System

Overview

The **Inventory Purchase & Vendor Management System** is a backend REST API built with **FastAPI**. It provides secure authentication, role-based authorization, vendor management, purchase order management, and reporting features. The application follows RESTful API principles and uses JWT authentication for secure access.


Features

Authentication & Authorization

* User Registration
* User Login
* JWT Authentication
* Password Hashing
* Role-Based Access Control

**Admin**

    * Manage Vendors
    * Manage Purchase Orders
  * **Store Manager**

    * Manage Purchase Orders Only

Vendor Management

* Create Vendor
* View All Vendors
* View Vendor by ID
* Update Vendor
* Soft Delete Vendor
* Unique Vendor Email Validation

Purchase Order Management

* Create Purchase Orders
* View All Purchase Orders
* View Purchase Order by ID
* Update Purchase Orders
* Automatic Total Amount Calculation

Reports

* Purchase History by Vendor
* Filter Orders by Status
* Search Orders by Product Name
* Pagination Support

Business Rules

* One Vendor can have Multiple Purchase Orders
* Purchase Orders cannot be created for Inactive Vendors
* Total Amount is automatically calculated (`Quantity × Unit Price`)
* Received Purchase Orders cannot be edited


Tech Stack

* Python 3.9+
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* JWT Authentication
* Passlib (bcrypt)
* Uvicorn
* Pytest


Project Structure

text
inventory_purchase_vendor_management_system/
│
├── routers/
│   ├── auth.py
│   ├── vendors.py
│   └── purchase_orders.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_vendors.py
│   └── test_purchase_orders.py
│
├── auth.py
├── database.py
├── dependencies.py
├── main.py
├── models.py
├── oauth2.py
├── schemas.py
├── requirements.txt
├── README.md
└── inventory.db

API Endpoints

Authentication

* `POST /auth/register`
* `POST /auth/login`

Vendor Management

* `POST /vendors`
* `GET /vendors`
* `GET /vendors/{vendor_id}`
* `PUT /vendors/{vendor_id}`
* `DELETE /vendors/{vendor_id}`

Purchase Order Management

* `POST /purchase-orders`
* `GET /purchase-orders`
* `GET /purchase-orders/{order_id}`
* `PUT /purchase-orders/{order_id}`

Reports

* Purchase History by Vendor
* Filter Orders by Status
* Search Orders by Product Name
* Pagination



Installation

Clone the Repository

bash
git clone <repository-url>
cd inventory_purchase_vendor_management_system


Create a Virtual Environment

bash
python -m venv venv


Activate the Virtual Environment

**Windows**

bash
venv\Scripts\activate


Install Dependencies

bash
pip install -r requirements.txt

Run the Application

bash
uvicorn main:app --reload


API Documentation

After running the application, open:


http://127.0.0.1:8000/docs




Testing

Run all test cases using:

bash
pytest


Validation & Security

* JWT Authentication
* Password Hashing
* Unique Vendor Email
* Quantity > 0
* Unit Price > 0
* Role-Based Authorization
* Soft Delete for Vendors


Future Improvements

* Inventory Stock Management
* Email Notifications
* Dashboard & Analytics
* Export Reports (PDF/Excel)
* Audit Logging


Author

Tharun
