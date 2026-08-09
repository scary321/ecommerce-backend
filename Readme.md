# E-Commerce Backend — Development Progress

## 📌 Project Overview

This project is a backend API for an e-commerce application built with **FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Alembic, and JWT authentication**.

The goal is to build a production-style e-commerce backend from scratch while learning backend development concepts such as authentication, authorization, database design, API architecture, testing, and deployment.

---

# 🚀 Development Progress

## Day 1 — Project Setup & FastAPI Fundamentals

### Implemented

- FastAPI project structure
- Application setup
- API routes
- Request and response handling
- Basic API testing with Swagger/OpenAPI
- PostgreSQL database connection
- SQLAlchemy setup
- Database session dependency

### Learned

- FastAPI fundamentals
- Dependency injection
- REST API basics
- SQLAlchemy basics
- PostgreSQL connection
- API request/response flow

---

## Day 2 — Database & User System

### Implemented

- Users database model
- User registration
- User response schemas
- Password hashing
- Database queries using SQLAlchemy
- User creation endpoint

### Learned

- SQLAlchemy models
- Pydantic schemas
- Password security
- Database CRUD operations
- Separation between database models and API schemas

---

## Day 3 — Authentication

### Implemented

- User login
- OAuth2 password flow
- JWT token generation
- JWT token validation
- Current-user dependency
- Protected endpoints

### Learned

- Authentication vs authorization
- JWT structure
- Access tokens
- OAuth2PasswordBearer
- FastAPI dependencies
- Protecting API routes

---

## Day 4 — User Account Management

### Implemented

- Get current user
- Update user information
- Password updates
- Email updates
- User account deletion
- Proper HTTP status codes
- Authentication-based access control

### Learned

- Partial updates
- `Optional` Pydantic fields
- `403 Forbidden`
- `404 Not Found`
- `204 No Content`
- Secure user-specific operations

---

# Day 5 — Role-Based Authorization & Admin Management

## 🎯 Objective

Upgrade the authentication system into a **role-based authorization system** and introduce administrator functionality.

## Implemented

### User Roles

Added a `role` field to the users table.

Supported roles:

- `user`
- `admin`

New users receive the `user` role by default.

### Database Migration

Created and applied an Alembic migration to add the role column.

Migration successfully applied using:

```bash
alembic upgrade head
```

### Admin Authorization

Implemented an admin authorization dependency:

```text
JWT
 ↓
get_current_user()
 ↓
Current User
 ↓
Check role
 ↓
Admin → Allow
User → 403
```

### Admin User Management

Implemented:

```text
GET    /users
PUT    /users/{id}
DELETE /users/{id}
```

Admins can:

- View all users
- Change a user's role
- Delete normal users

Security restrictions:

- Normal users cannot access admin endpoints
- Admins cannot delete themselves
- Admins cannot delete another admin

### API Status Codes

Implemented and tested:

| Status           | Usage                  |
| ---------------- | ---------------------- |
| `200 OK`         | Successful requests    |
| `201 Created`    | User creation          |
| `204 No Content` | Successful deletion    |
| `403 Forbidden`  | Unauthorized operation |
| `404 Not Found`  | Resource doesn't exist |

### Debugging

Fixed duplicate route definitions for:

```text
DELETE /users/{id}
```

This prevented conflicting user-delete and admin-delete behavior.

---

# 📊 Current Backend Architecture

```text
Client
  ↓
FastAPI
  ↓
Authentication
  ↓
JWT
  ↓
get_current_user()
  ↓
Authorization
  ↓
require_admin()
  ↓
API Routes
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

---

# ✅ Current Features

### Authentication

- [x] User registration
- [x] Password hashing
- [x] User login
- [x] JWT authentication
- [x] Protected routes
- [x] Current-user dependency

### User Management

- [x] Get user
- [x] Update user
- [x] Delete user
- [x] Email update
- [x] Password update

### Authorization

- [x] User roles
- [x] Admin role
- [x] Admin dependency
- [x] Admin-only routes
- [x] User/admin permissions

### Admin Management

- [x] View all users
- [x] Update user role
- [x] Delete normal users
- [x] Prevent admin self-deletion
- [x] Prevent admin-to-admin deletion

### Database

- [x] PostgreSQL
- [x] SQLAlchemy
- [x] Alembic migrations
- [x] User table
- [x] Role column

---

# 🔜 Next — Day 6

## Product Management

The next major feature is the **Product system**, which will move the project from mainly user/authentication functionality into actual e-commerce functionality.

### Planned

- [ ] Create Product model
- [ ] Product database table
- [ ] Alembic migration
- [ ] Product schemas
- [ ] Create product endpoint
- [ ] Get all products
- [ ] Get single product
- [ ] Update product
- [ ] Delete product
- [ ] Admin-only product management
- [ ] Product validation
- [ ] Product stock management
- [ ] Product categories

### Planned API

```text
POST   /products
GET    /products
GET    /products/{id}
PUT    /products/{id}
DELETE /products/{id}
```

### Planned Permissions

```text
                    USER        ADMIN

View products        ✅          ✅
Create product       ❌          ✅
Update product       ❌          ✅
Delete product       ❌          ✅
```

---

# 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **Alembic**
- **JWT**
- **OAuth2**
- **Passlib / Password Hashing**
- **Swagger / OpenAPI**

---

# 🎯 Project Goal

Build a complete e-commerce backend from scratch with:

```text
Authentication
      ↓
Authorization
      ↓
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
Testing
      ↓
Docker
      ↓
CI/CD
      ↓
Deployment
```

The project is being developed incrementally, with each development day introducing and testing a new backend concept.
