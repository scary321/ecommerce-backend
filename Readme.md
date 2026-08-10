# E-Commerce Backend — Day 6

## 📌 Project Overview

This project is a backend API for an e-commerce application built with **FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pydantic, and JWT authentication**.

The project is being developed step-by-step, with each day adding a new part of the backend.

By the end of Day 6, the backend has a working **user authentication/authorization system** and a complete **Product CRUD system**.

---

# ✅ What Has Been Implemented

## 👤 User Management

User functionality has already been implemented.

### User Features

- User registration
- User login
- Password hashing
- Password verification
- JWT access tokens
- Get current user
- Get user by ID
- Update user
- Delete own account
- Admin user listing
- Admin role updates
- Admin user deletion
- Admin authorization

### User Roles

The application currently supports:

- `user`
- `admin`

Admins have additional permissions over users and products.

---

# 🔐 Authentication & Authorization

JWT authentication is implemented.

The authentication flow is:

```text
Login
  ↓
Email + Password
  ↓
Verify credentials
  ↓
Generate JWT
  ↓
Client sends Bearer Token
  ↓
get_current_user()
  ↓
Identify user
  ↓
require_admin()
  ↓
Check role
```

### Authorization

Admin-only operations are protected using:

```text
Depends(require_admin)
```

Normal users cannot access admin-only operations.

---

# 🛍️ Product Management

Day 6 introduced the Product Management system.

## Product Model

The `products` database table contains:

- `id`
- `name`
- `description`
- `price`
- `stock`
- `category`
- `created_at`

The Product model is separated from the User model.

---

# 📦 Product CRUD

The Product API currently supports complete CRUD operations.

| Method | Endpoint         | Purpose          | Access        |
| ------ | ---------------- | ---------------- | ------------- |
| POST   | `/products`      | Create product   | Admin         |
| GET    | `/products`      | Get all products | Authenticated |
| GET    | `/products/{id}` | Get one product  | Authenticated |
| PATCH  | `/products/{id}` | Update product   | Admin         |
| DELETE | `/products/{id}` | Delete product   | Admin         |

---

## ✅ Create Product

```text
POST /products
```

Admins can create products.

Status:

```text
201 Created
```

---

## ✅ Get All Products

```text
GET /products
```

Authenticated users can retrieve all products.

---

## ✅ Get Product

```text
GET /products/{id}
```

Returns a specific product.

If the product doesn't exist:

```text
404 Product not found
```

---

## ✅ Update Product

```text
PATCH /products/{id}
```

Admins can partially update products.

For example, only changing:

```json
{
  "price": 1499
}
```

will leave the other product fields unchanged.

Partial updates use:

```text
model_dump(exclude_unset=True)
```

---

## ✅ Delete Product

```text
DELETE /products/{id}
```

Admins can delete products.

Successful deletion returns:

```text
204 No Content
```

---

# 🗄️ Database

PostgreSQL is being used as the main database.

SQLAlchemy is used as the ORM.

Alembic is used for database migrations.

The Product table was successfully created using:

```bash
alembic revision --autogenerate -m "add products table"
```

and:

```bash
alembic upgrade head
```

---

# 📁 Current Project Structure

```text
E-commerce backend/
│
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── products.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── products.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── products.py
│   │
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── utils.py
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── ...
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

# 🧪 Testing Status

The implemented functionality has been tested using **FastAPI Swagger UI**.

### Tested

- ✅ User registration
- ✅ User login
- ✅ JWT authentication
- ✅ Admin authorization
- ✅ Normal user restrictions
- ✅ Product creation
- ✅ Product listing
- ✅ Individual product retrieval
- ✅ Product partial update
- ✅ Product deletion
- ✅ Invalid product ID
- ✅ `403 Forbidden`
- ✅ `404 Not Found`
- ✅ `204 No Content`

---

# ❌ What Is NOT Implemented Yet

The backend is **not a complete e-commerce application yet**.

The following major features are still pending:

## 🛒 Shopping Cart

Not implemented yet:

- Cart model
- Cart items
- Add product to cart
- Remove product from cart
- Update quantity
- View cart
- Calculate cart total

## 📦 Orders

Not implemented yet:

- Order model
- Order items
- Create order
- Order status
- Order history
- Cancel order

## 💳 Payments

Not implemented yet:

- Payment integration
- Payment verification
- Payment status
- Failed payment handling

## 📊 Product Improvements

Not implemented yet:

- Product search
- Product filtering
- Product sorting
- Pagination
- Product images
- Product reviews/ratings

## 📦 Inventory

Not implemented yet:

- Automatic stock reduction
- Stock validation
- Out-of-stock handling
- Inventory tracking

---

# 🚧 Current Project Status

```text
Authentication        ██████████ 100%
Authorization         ██████████ 100%
User Management       ██████████ 100%
Product CRUD          ██████████ 100%
Database Migrations    ██████████ 100%
Shopping Cart         ░░░░░░░░░░   0%
Orders                ░░░░░░░░░░   0%
Payments              ░░░░░░░░░░   0%
Inventory             ░░░░░░░░░░   0%
Search & Filtering    ░░░░░░░░░░   0%
Deployment            ░░░░░░░░░░   0%
```

The project is currently in the **core backend/API development stage**.

---

# 📚 Day 6 Learning

Day 6 focused on:

- Product CRUD
- FastAPI routers
- Separating models and schemas
- SQLAlchemy queries
- Alembic migrations
- JWT authentication
- Role-based authorization
- PATCH vs PUT
- Partial updates
- `model_dump(exclude_unset=True)`
- Dynamic updates using `setattr()`
- HTTP status codes
- Swagger API testing

---

# 🔜 Next Steps

The next development stage will continue building the actual e-commerce functionality.

Potential next features:

1. Shopping cart
2. Cart items
3. Product quantity management
4. Order creation
5. Order history
6. Inventory management
7. Payment integration
8. Product search/filtering
9. Pagination
10. Testing with Pytest
11. Docker
12. CI/CD
13. Deployment

---

# 🎯 Current Goal

The immediate goal is to move from a basic **User + Product API** into a complete e-commerce backend by implementing:

```text
Users
  ↓
Products
  ↓
Cart
  ↓
Orders
  ↓
Payments
  ↓
Inventory
```

The project will continue to be developed incrementally, with each day's work documented in the README.
