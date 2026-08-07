# 🛒 E-Commerce Backend API

A backend API for an e-commerce application built with **FastAPI**.
The project is being developed step-by-step while learning backend development, database integration, authentication, testing, and deployment.

## 📌 Project Overview

This project focuses on building a production-style e-commerce backend from scratch using Python and FastAPI.

The goal is to implement the core backend features required for an e-commerce platform, including:

- User registration and authentication
- Database management
- JWT-based authorization
- Product management
- Orders
- User permissions
- API validation
- Testing
- Deployment

---

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

### Database

- PostgreSQL

### Authentication & Security

- JWT
- OAuth2 Bearer Authentication
- Password Hashing
- Password Verification

### Development & Testing

- Swagger / OpenAPI
- Pytest
- Virtual Environment
- Git & GitHub

### Planned / Learning

- Docker
- GitHub Actions
- Deployment

---

## ✅ Completed

### User Management

- [x] User registration
- [x] User database model
- [x] User response schema
- [x] Password hashing
- [x] Password verification
- [x] Get user by ID

### Authentication

- [x] Login endpoint
- [x] JWT access token generation
- [x] JWT expiration
- [x] JWT decoding
- [x] `OAuth2PasswordBearer`
- [x] `OAuth2PasswordRequestForm`
- [x] `get_current_user()` dependency
- [x] Protected endpoints
- [x] Swagger OAuth2 authentication

### API

- [x] FastAPI application setup
- [x] Database session dependency
- [x] Pydantic request/response validation
- [x] HTTP status codes
- [x] Error handling for authentication and missing users

---

## 🚧 Currently Working On

- [ ] User authorization
- [ ] User ownership/permissions
- [ ] Product CRUD
- [ ] Product categories
- [ ] Shopping cart
- [ ] Orders
- [ ] Order items
- [ ] Advanced API validation
- [ ] Automated tests

---

## ❌ Not Implemented Yet

The following features are planned but have not been implemented yet:

- Product management
- Cart system
- Checkout system
- Order management
- Payment integration
- Admin roles
- Role-based access control
- Product search and filtering
- Pagination
- Email verification
- Password reset
- Refresh tokens
- Production deployment
- Docker production setup
- CI/CD pipeline

---

## 🔐 Current Authentication Flow

```text
Register User
      ↓
Hash Password
      ↓
Store User in PostgreSQL
      ↓
Login
      ↓
Verify Password
      ↓
Generate JWT
      ↓
Bearer Token
      ↓
Protected Endpoint
      ↓
Get Current User
```

---

## 📚 Learning Progress

| Area               | Status |
| ------------------ | ------ |
| Python Backend     | ✅     |
| FastAPI Basics     | ✅     |
| SQLAlchemy         | ✅     |
| PostgreSQL         | ✅     |
| User Registration  | ✅     |
| Password Hashing   | ✅     |
| JWT Authentication | ✅     |
| OAuth2             | ✅     |
| Protected Routes   | ✅     |
| Authorization      | 🚧     |
| Product APIs       | ⏳     |
| Cart               | ⏳     |
| Orders             | ⏳     |
| Testing            | ⏳     |
| Docker             | ⏳     |
| Deployment         | ⏳     |
| CI/CD              | ⏳     |

---

## 📂 Project Structure

```text
E-commerce backend/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   └── utils.py
│
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> Project structure may change as development continues.

---

## 🚀 Running Locally

Create and activate a virtual environment:

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 📈 Project Status

**Development Status: 🟡 In Progress**

The core backend foundation and user authentication system are working.
The next major step is implementing **authorization and user permissions**, followed by the main e-commerce functionality.

---

## 🎯 Next Goal

### Day 5

**Authorization & User Permissions 🔒**

After that, the project will move toward:

```text
Authentication
      ↓
Authorization
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
Deployment
```
