# 🛒 E-Commerce Backend API

A backend REST API for an e-commerce application built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Pydantic**, and **JWT authentication**.

The project is being developed step-by-step with a focus on building a production-style e-commerce backend from scratch.

## 🚀 Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **JWT Authentication**
- **Alembic**
- **Pytest**
- **Docker**
- **Git & GitHub**

## 📌 Current Features

### Authentication & Users

- User registration
- User login
- JWT authentication
- Protected API routes
- Current-user dependency

### Products

- Product management
- Product stock tracking
- Product pricing
- Product availability checking

### Cart

- Create/get user cart
- Add products to cart
- Update cart items
- Remove cart items
- Cart ownership protection
- Stock validation

### Orders

The Day 10 milestone completes the main order-management flow.

- Create an order from the user's cart
- Calculate order total
- Create order items
- Reduce product stock after purchase
- Automatically clear the cart after order creation
- Get all orders belonging to the current user
- Get a specific order
- Protect orders from other users
- Update order status
- Validate order status transitions
- Cancel orders
- Restore product stock when an order is cancelled

## 📦 Order Status Flow

Orders currently support:

```text
pending
   ↓
processing
   ↓
shipped
   ↓
delivered
```

Cancellation is allowed from:

```text
pending → cancelled
processing → cancelled
```

Invalid transitions are rejected by the API.

## 🗂️ Project Structure

```text
app/
├── models/
│   ├── users.py
│   ├── products.py
│   ├── carts.py
│   └── orders.py
│
├── schemas/
│   ├── users.py
│   ├── products.py
│   ├── carts.py
│   └── order.py
│
├── routers/
│   ├── users.py
│   ├── products.py
│   ├── carts.py
│   └── orders.py
│
├── database.py
├── config.py
└── main.py

alembic/
requirements.txt
.env
README.md
```

## 🔐 API Security

Protected endpoints use JWT authentication.

The authenticated user is obtained through the `get_current_user` dependency.

Order endpoints verify that the requested order belongs to the authenticated user before allowing access or modification.

## 🛍️ Order Creation Flow

The order creation process works approximately like this:

```text
User Cart
   ↓
Get Cart Items
   ↓
Check Product Stock
   ↓
Calculate Total
   ↓
Create Order
   ↓
Create Order Items
   ↓
Reduce Product Stock
   ↓
Clear Cart
   ↓
Commit Transaction
```

## ❌ Order Cancellation Flow

```text
Cancel Request
      ↓
Find User's Order
      ↓
Check Status
      ↓
pending / processing?
      ↓
Restore Product Stock
      ↓
Set Status = cancelled
      ↓
Commit
```

The order is **not deleted**, preserving the user's order history.

## 📋 Example Order Response

```json
{
  "id": 1,
  "total": 20,
  "status": "pending",
  "created_at": "2026-08-13T15:20:31.433528",
  "items": [
    {
      "id": 1,
      "product_id": 3,
      "quantity": 2,
      "price": 10
    }
  ]
}
```

## 🧪 Testing

The project uses **Pytest** for API and backend testing.

Tests cover areas such as:

- Authentication
- Users
- Products
- Cart functionality
- Orders
- Database interactions

Run tests with:

```bash
pytest
```

## 🗄️ Database Migrations

Alembic is used to manage database schema changes.

Create a migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
alembic upgrade head
```

## ▶️ Running the Project

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

API documentation is available through FastAPI's Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## 🐳 Docker

The project also includes Docker support for running the backend and PostgreSQL database in containers.

## 🛣️ Development Roadmap

Current progress:

- [x] Authentication
- [x] Users
- [x] Products
- [x] Cart
- [x] Order creation
- [x] Order retrieval
- [x] Order status management
- [x] Order cancellation
- [x] Stock restoration
- [ ] Advanced order features
- [ ] Admin functionality
- [ ] Payment integration
- [ ] Email notifications
- [ ] Improved automated testing
- [ ] Production deployment
- [ ] CI/CD improvements

## 📅 Current Milestone

**Day 10 — Order Management completed ✅**

The project now has a complete basic purchasing workflow:

```text
User
 ↓
Product
 ↓
Cart
 ↓
Order
 ↓
Order Items
 ↓
Stock Management
 ↓
Order Status
 ↓
Cancellation
```

## 👨‍💻 Author

**Priyanshu**

This project is being developed as a hands-on backend engineering project to strengthen skills in **Python, FastAPI, PostgreSQL, SQLAlchemy, REST APIs, authentication, testing, Docker, and deployment**.
