# 🛒 E-commerce Backend API

A production-ready E-commerce Backend built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**. This project is being developed from scratch following backend engineering best practices, including authentication, database migrations, password hashing, and RESTful API design.

---

## 🚀 Tech Stack

- **FastAPI** – High-performance Python web framework
- **PostgreSQL** – Relational database
- **SQLAlchemy** – ORM for database operations
- **Alembic** – Database migrations
- **Pydantic** – Data validation and serialization
- **Passlib (bcrypt)** – Secure password hashing
- **Uvicorn** – ASGI server
- **Python 3.13**

---

## ✨ Features Implemented

### ✅ Project Setup

- FastAPI application structure
- Environment variable configuration
- PostgreSQL database connection
- SQLAlchemy ORM setup
- Dependency Injection with `Depends(get_db)`

### ✅ Database

- User model created
- Alembic configured
- Initial database migration
- Automatic timestamps (`created_at`)

### ✅ User Management

- User registration endpoint
- Request validation using Pydantic
- Response schemas to hide sensitive information
- Secure password hashing using bcrypt
- Passwords are never stored in plain text

---

## 📂 Project Structure

```text
app/
├── config.py          # Environment variables
├── database.py        # Database engine & session
├── main.py            # FastAPI application
├── models.py          # SQLAlchemy models
├── schemas.py         # Pydantic schemas
├── utils.py           # Password hashing utilities
└── ...

alembic/
├── versions/          # Migration files
└── env.py

requirements.txt
README.md
```

---

## 🛠 Installation

### Clone the repository

```bash
git clone https://github.com/scary321/ecommerce-backend.git
cd ecommerce-backend
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙ Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_database
DATABASE_USERNAME=your_username
DATABASE_PASSWORD=your_password

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## ▶ Running the Project

```bash
uvicorn app.main:app --reload
```

API Documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## 📌 Current API Endpoints

| Method | Endpoint | Description         |
| ------ | -------- | ------------------- |
| GET    | `/`      | Health check        |
| POST   | `/users` | Register a new user |

---

## 📈 Roadmap

- ✅ User Registration
- 🔄 User Login (JWT Authentication)
- ⏳ Protected Routes
- ⏳ Product APIs
- ⏳ Category APIs
- ⏳ Shopping Cart
- ⏳ Orders
- ⏳ Payment Integration
- ⏳ Unit Testing
- ⏳ Docker
- ⏳ CI/CD
- ⏳ Deployment

---

## 🔒 Security

- Passwords hashed using bcrypt
- Request validation with Pydantic
- Response models prevent sensitive data exposure
- Environment variables for secrets and database credentials

---

## 👨‍💻 Author

**Priyanshu Rathore**

GitHub: https://github.com/scary321
