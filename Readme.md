# 🛒 E-Commerce Backend API

A production-oriented **E-Commerce Backend API** built with **FastAPI, PostgreSQL, SQLAlchemy, Pydantic, JWT Authentication, and Alembic**.

This project is being developed step-by-step as a complete backend system, focusing not only on CRUD operations but also on **authentication, authorization, database relationships, inventory management, order processing, role-based access control, and admin functionality**.

---

## 🚀 Project Overview

The goal of this project is to build a realistic e-commerce backend from scratch.

The API currently supports:

- User registration and login
- JWT-based authentication
- Password hashing
- User profile management
- Product management
- Product categories and inventory
- Shopping cart functionality
- Order creation
- Order items
- Stock management
- Order status management
- Order cancellation
- Stock restoration after cancellation
- Role-based authorization
- Admin user management
- Admin product management
- Admin order management
- Order filtering
- Admin dashboard statistics
- Total sales calculation

---

## 🛠️ Tech Stack

| Technology                     | Purpose                       |
| ------------------------------ | ----------------------------- |
| **Python**                     | Backend programming language  |
| **FastAPI**                    | REST API framework            |
| **PostgreSQL**                 | Relational database           |
| **SQLAlchemy**                 | ORM / database interaction    |
| **Pydantic**                   | Request & response validation |
| **JWT**                        | Authentication                |
| **Alembic**                    | Database migrations           |
| **Passlib / Password Hashing** | Secure password storage       |
| **Swagger / OpenAPI**          | API testing and documentation |
| **Docker**                     | Containerization              |

---

# 📁 Project Structure

```text
app/
├── models/
│   ├── user.py
│   ├── products.py
│   ├── cart.py
│   ├── orders.py
│   └── ...
│
├── schemas/
│   ├── user.py
│   ├── product.py
│   ├── order.py
│   └── dashboard.py
│
├── routers/
│   ├── users.py
│   ├── products.py
│   ├── orders.py
│   ├── admin.py
│   └── ...
│
├── auth.py
├── database.py
├── config.py
├── utils.py
└── main.py

alembic/
├── versions/
└── env.py

tests/
requirements.txt
Dockerfile
```

---

# 🔐 Authentication & Authorization

The project uses **JWT-based authentication**.

### Authentication flow

```text
User Login
    ↓
Verify email/password
    ↓
Create JWT
    ↓
Client sends JWT
    ↓
get_current_user()
    ↓
Identify authenticated user
```

The JWT contains the user's ID, which is used to retrieve the user from the database.

Passwords are never stored as plain text. They are stored as hashed passwords.

---

# 👤 User Management

Users can:

- Register
- Login
- View their profile
- Update their information
- Delete their account

Users can only access or modify their own protected resources.

For example:

```text
GET /users/{id}
PATCH /users/{id}
DELETE /users/me/{id}
```

Authorization checks ensure that one user cannot modify another user's account.

---

# 📦 Product Management

The API supports product CRUD operations.

### Admin

Admins can:

- Create products
- Update products
- Delete products
- Manage stock
- Manage product information

### Authenticated users

Users can:

- View all products
- View an individual product

Example endpoints:

```text
POST   /products
GET    /products
GET    /products/{id}
PATCH  /products/{id}
DELETE /products/{id}
```

---

# 🛒 Cart & Inventory

The cart system connects users with products.

A cart can contain multiple products, and products can exist in multiple carts.

Stock is checked before an order is created.

This prevents customers from ordering more products than are available.

---

# 📦 Order System

The project uses two important database concepts:

### Order

Represents the overall purchase.

Example:

```text
Order
├── id
├── user_id
├── total
├── status
└── created_at
```

### OrderItem

Represents individual products inside an order.

```text
OrderItem
├── id
├── order_id
├── product_id
├── quantity
└── price
```

One order can contain multiple order items.

For example:

```text
Order #3
│
├── Product #1 × 15
└── Product #3 × 15
```

This separation makes the database structure flexible and realistic.

---

# 🔄 Order Status

The project supports:

```text
pending
processing
shipped
delivered
cancelled
```

For normal users, status transitions are controlled.

```text
pending
   ├── processing
   └── cancelled

processing
   ├── shipped
   └── cancelled

shipped
   └── delivered

delivered
   └── final

cancelled
   └── final
```

This prevents invalid order transitions.

---

# ❌ Order Cancellation

Users can cancel eligible orders.

When an order is cancelled:

```text
Order cancelled
      ↓
Get OrderItems
      ↓
Find Products
      ↓
Restore quantity to stock
      ↓
Update order status
      ↓
Commit transaction
```

For example:

```text
Product stock = 15
Order quantity = 5

After order:
Stock = 10

After cancellation:
Stock = 15
```

This prevents inventory from being permanently reduced by cancelled orders.

The API also prevents:

- Cancelling an already cancelled order
- Cancelling a delivered order
- Restoring the same stock multiple times

---

# 👑 Admin System

The project includes **role-based access control**.

Users have a role such as:

```text
user
admin
```

A reusable `require_admin()` dependency checks the authenticated user's role.

```text
Request
   ↓
JWT authentication
   ↓
get_current_user()
   ↓
require_admin()
   ↓
role == "admin"?
   ├── Yes → Continue
   └── No  → 403 Forbidden
```

This prevents normal users from accessing administrative functionality.

---

# 👨‍💼 Admin User Management

Admins can:

- View all users
- Change user roles
- Delete users

Additional protections include:

- Admin cannot delete themselves
- Admin cannot delete another admin

---

# 📋 Admin Order Management

Admins can view orders belonging to **all users**.

```text
GET /admin/orders
```

Unlike the normal user order endpoint, the admin endpoint does not restrict orders by the current user's ID.

### Status filtering

The same endpoint supports optional filtering:

```text
GET /admin/orders
GET /admin/orders?status=pending
GET /admin/orders?status=processing
GET /admin/orders?status=shipped
GET /admin/orders?status=delivered
GET /admin/orders?status=cancelled
```

Invalid statuses are rejected.

---

# 🔧 Admin Order Status Management

Admins have more control over order status than normal users.

Admins can change an order to any valid status:

```text
pending
processing
shipped
delivered
cancelled
```

This allows administrative corrections and management of orders.

---

# 🚫 Admin Order Cancellation

Admins can cancel orders using a dedicated endpoint.

When an admin cancels an order:

```text
Admin
 ↓
Find Order
 ↓
Check order status
 ↓
Get OrderItems
 ↓
Restore Product Stock
 ↓
Set status = cancelled
 ↓
Commit
```

Delivered orders cannot be cancelled, and already-cancelled orders cannot be cancelled again.

---

# 📊 Admin Dashboard

The project includes an admin dashboard endpoint:

```text
GET /admin/dashboard
```

It provides:

```text
Total Users
Total Products
Total Orders

Pending Orders
Processing Orders
Shipped Orders
Delivered Orders
Cancelled Orders

Total Sales
```

Example conceptual response:

```json
{
  "users": 10,
  "products": 25,
  "orders": 50,
  "pending_orders": 5,
  "processing_orders": 8,
  "shipped_orders": 12,
  "delivered_orders": 20,
  "cancelled_orders": 5,
  "sales": 12500.0
}
```

Cancelled orders are excluded from the total sales calculation.

---

# 📚 Day 11 — Theory

## 1. Role-Based Access Control (RBAC)

RBAC means giving users different permissions based on their role.

Example:

```text
User
 ├── View products
 ├── Manage own cart
 └── Manage own orders

Admin
 ├── Manage users
 ├── Manage products
 ├── Manage orders
 └── View dashboard
```

Instead of checking permissions manually in every endpoint, a reusable dependency such as `require_admin()` centralizes authorization.

---

## 2. Authentication vs Authorization

These are different concepts.

### Authentication

Answers:

> Who are you?

JWT authentication identifies the current user.

### Authorization

Answers:

> What are you allowed to do?

The user's `role` determines whether they can access admin functionality.

```text
Authentication
     ↓
Who is the user?

Authorization
     ↓
What can the user do?
```

---

## 3. Query Parameters

Day 11 introduced filtering using query parameters.

Instead of creating separate endpoints:

```text
/admin/pending-orders
/admin/shipped-orders
/admin/cancelled-orders
```

we use:

```text
/admin/orders?status=pending
/admin/orders?status=shipped
/admin/orders?status=cancelled
```

The endpoint remains the same while the query parameter changes the filtering.

This pattern is useful for:

- Filtering
- Searching
- Sorting
- Pagination

---

## 4. SQLAlchemy Query Building

The dashboard uses database queries such as:

```text
query → filter → count
```

For example:

```text
OrderTable
    ↓
filter(status == "pending")
    ↓
count()
```

For sales:

```text
OrderTable
    ↓
exclude cancelled orders
    ↓
sum(total)
```

The important concept is that a query can be built and modified before it is executed.

---

## 5. Aggregation

The admin dashboard introduced database aggregation.

Common aggregation functions include:

```text
COUNT()
SUM()
AVG()
MIN()
MAX()
```

In this project:

```text
COUNT → users/products/orders
SUM   → total sales
```

This allows the database to calculate statistics efficiently.

---

## 6. Inventory Consistency

A major concept in Day 11 was keeping inventory consistent.

When an order is created:

```text
Stock decreases
```

When an order is cancelled:

```text
Stock increases again
```

This prevents cancelled orders from incorrectly reducing available inventory.

---

## 7. Business Rules

The API isn't just CRUD.

It contains business rules such as:

```text
Delivered order cannot be cancelled
Cancelled order cannot be cancelled again
Invalid status cannot be assigned
Normal users cannot access admin endpoints
Admins can manage all users/orders
```

These rules make the backend behave like a real application.

---

## 8. API Response Schemas

`DashboardResponse` is a Pydantic schema used to define exactly what the dashboard returns.

Instead of returning arbitrary data, FastAPI validates the response against the schema.

This provides:

- Data validation
- Consistent API responses
- Automatic Swagger documentation
- Better API contracts

---

# 🧪 Testing

The API has been tested using **FastAPI Swagger / OpenAPI documentation**.

Swagger is available during development through:

```text
/docs
```

Testing includes:

- Authentication
- User endpoints
- Product endpoints
- Cart/order flows
- Order status transitions
- Cancellation
- Stock restoration
- Admin authorization
- Admin order filtering
- Admin status updates
- Admin dashboard

---

# 🗓️ Development Progress

```text
Day 1  → Project foundation                  ✅
Day 2  → Database & models                   ✅
Day 3  → Authentication                     ✅
Day 4  → Users                               ✅
Day 5  → Products                            ✅
Day 6  → Cart                                ✅
Day 7  → Cart & inventory flow               ✅
Day 8  → Orders & relationships              ✅
Day 9  → Order status management             ✅
Day 10 → Cancellation & stock handling       ✅
Day 11 → Admin system & dashboard            ✅
Day 12 → Payments                             ⏳
Day 13 → Testing & edge cases                ⏳
Day 14 → Docker & production setup           ⏳
Day 15 → Deployment & final polish           ⏳
```

---

# 🎯 Current Project Status

**Day 11 completed successfully.**

The backend now contains realistic e-commerce functionality including:

**Authentication → Users → Products → Cart → Orders → Inventory → Order Lifecycle → Admin → Dashboard**

The next stage will focus on **payment integration, deeper testing, production readiness, and deployment**.

---

## 👨‍💻 Author

**Priyanshu Rathore**

Built as a hands-on backend development project using FastAPI and PostgreSQL.
