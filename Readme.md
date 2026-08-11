# E-Commerce Backend

### Project Overview

This project is a **backend API for an E-Commerce application** built using **FastAPI, SQLAlchemy, PostgreSQL, Pydantic, JWT authentication, and Alembic**.

The goal is to build a complete backend where users can:

- Register and log in
- Authenticate using JWT tokens
- Manage their profile
- Browse products
- Add products to a shopping cart
- Update cart quantities
- Remove products from the cart
- Place orders
- Track their orders
- Eventually complete payments

Admins can:

- Manage users
- Manage products
- Manage orders

---

# 🗺️ Project Progress

```text
FastAPI
   ↓
Database / PostgreSQL
   ↓
Users
   ↓
Authentication
   ↓
JWT Authorization
   ↓
Admin Authorization
   ↓
Products
   ↓
🛒 Shopping Cart ← DAY 7
   ↓
📦 Orders / Checkout
   ↓
💳 Payments
   ↓
🧪 Testing
   ↓
🚀 Deployment
```

---

# ✅ What I Completed Before Day 7

## Users

Implemented user functionality:

- User registration
- Password hashing
- User login
- JWT access token generation
- Get current user
- Update user
- Delete user
- Admin user management
- Admin role management
- Admin authorization

---

## Products

Implemented product functionality:

- Create product
- Get all products
- Get individual product
- Update product
- Delete product
- Admin-only product management
- Product stock
- Product category
- Product price

---

# 🛒 What I Completed on Day 7

Day 7 focused on building the **Shopping Cart system**.

## 1. Cart Models

Created:

- `CartTable`
- `CartItemTable`

The database structure is:

```text
User
 ↓
Cart
 ↓
CartItem
 ↓
Product
```

---

## 2. Cart Database Migration

Created an Alembic migration for:

```text
carts
cart_items
```

The migration was successfully applied to the database.

---

## 3. Cart Schemas

Created schemas for:

### CartItemCreate

Used when adding a product:

```text
product_id
quantity
```

### CartItemUpdate

Used when updating quantity:

```text
quantity
```

### CartItemResponse

Used to return cart item information.

### CartResponse

Used to return:

```text
cart id
items
total
```

---

# 4. Add Product to Cart

Implemented:

```text
POST /cart/items
```

The endpoint:

1. Finds the product.
2. Checks whether the product exists.
3. Validates quantity.
4. Checks product stock.
5. Finds the user's cart.
6. Creates a cart if the user doesn't have one.
7. Checks if the product already exists in the cart.
8. Increases quantity if it already exists.
9. Creates a new cart item otherwise.
10. Saves the changes.

---

# 5. Stock Validation

Implemented stock checking.

Example:

```text
Product stock = 10
Requested quantity = 5

5 <= 10
✓ Allowed
```

But:

```text
Product stock = 10
Requested quantity = 15

15 > 10
✗ Rejected
```

Also handled the case where an existing cart quantity plus the requested quantity would exceed stock.

---

# 6. Prevent Duplicate Cart Items

If the user already has:

```text
iPhone × 2
```

and adds:

```text
iPhone × 3
```

the system changes it to:

```text
iPhone × 5
```

instead of creating two separate cart items.

---

# 7. View Cart

Implemented:

```text
GET /cart
```

The endpoint:

- Finds the logged-in user's cart
- Gets all cart items
- Finds the corresponding products
- Calculates item subtotals
- Calculates the total cart value

Example:

```text
Product A
₹500 × 2 = ₹1,000

Product B
₹200 × 3 = ₹600

Total = ₹1,600
```

---

# 8. Update Cart Item

Implemented:

```text
PATCH /cart/items/{product_id}
```

Allows users to change the quantity of an item.

Example:

```text
Before:
Mouse × 2

Update:
quantity = 5

After:
Mouse × 5
```

The new quantity is checked against available stock.

---

# 9. Remove Cart Item

Implemented:

```text
DELETE /cart/items/{product_id}
```

This removes the product from the user's cart.

It does **not** delete the actual product.

```text
CartItem → deleted
Product  → remains
```

---

# 10. Clear Cart

Implemented:

```text
DELETE /cart
```

This removes all cart items belonging to the current user's cart.

The cart itself remains in the database.

---

# 🔐 Authorization in Cart

Cart operations use:

```text
get_current_user
```

This ensures users can only modify **their own cart**.

Admin authorization is not required because users are allowed to manage their own shopping cart.

---

# 🧠 Day 7 Theory

## 1. What Is a Shopping Cart?

A shopping cart is temporary user-specific data that stores products a user intends to purchase.

Example:

```text
User #10
   ↓
Cart #5
   ↓
Cart Items
├── Product #2 × 3
├── Product #7 × 1
└── Product #10 × 2
```

---

# 2. Why Do We Need CartItem?

We don't directly connect:

```text
Cart → Product
```

because we need additional information such as:

```text
quantity
```

Therefore:

```text
Cart
 ↓
CartItem
 ↓
Product
```

For example:

```text
CartItem
product_id = 5
quantity = 3
```

means:

> The user has 3 units of product #5 in their cart.

---

# 3. Foreign Keys

Foreign keys connect tables.

Example:

```text
cart_items.cart_id
        ↓
carts.id
```

and:

```text
cart_items.product_id
        ↓
products.id
```

This creates relationships between database tables.

---

# 4. One-to-Many Relationship

One cart can contain many cart items.

```text
Cart
 ├── CartItem
 ├── CartItem
 └── CartItem
```

Similarly, a product can appear in many different users' carts.

This is why relational database design is important in an e-commerce application.

---

# 5. Authentication vs Authorization

### Authentication

Answers:

> Who is the user?

JWT authentication identifies the logged-in user.

### Authorization

Answers:

> What is this user allowed to do?

For the cart:

```text
JWT
 ↓
get_current_user
 ↓
current_user.id
 ↓
Find user's cart
```

This prevents one user from accessing another user's cart.

---

# 6. Business Logic

Business logic represents the rules of the application.

Examples from Day 7:

### Stock rule

```text
requested quantity <= available stock
```

### Duplicate product rule

```text
Product already in cart
        ↓
Increase quantity
```

Otherwise:

```text
Create new CartItem
```

### Ownership rule

```text
Cart.user_id == current_user.id
```

These rules make the API behave like a real e-commerce application.

---

# 7. Database Transactions

Important SQLAlchemy operations:

### `db.add()`

Adds a new database object.

### `db.delete()`

Marks an object for deletion.

### `db.commit()`

Saves the transaction to the database.

### `db.refresh()`

Refreshes the object with the latest database state.

---

# 8. `.first()` vs `.all()`

### `.first()`

Use when you expect one result.

Example:

```text
Find user's cart
```

Returns:

```text
Cart object
```

or:

```text
None
```

### `.all()`

Use when multiple records are expected.

Example:

```text
Get all items in a cart
```

Returns:

```text
[CartItem, CartItem, CartItem]
```

---

# 9. Cart Total Calculation

The cart total is calculated from the products.

Formula:

```text
subtotal = product price × quantity
```

Then:

```text
total = subtotal₁ + subtotal₂ + subtotal₃ + ...
```

Example:

```text
₹1,000
+ ₹500
+ ₹2,000
= ₹3,500
```

---

# 10. Why Product and Cart Are Separate

A product belongs to the store's inventory.

A cart belongs to a particular user.

Therefore:

```text
Product
 ↓
Store inventory

Cart
 ↓
User's temporary selection
```

Deleting a cart item must not delete the actual product.

---

# 11. Why `CartItem` Is Important in E-Commerce

The `CartItem` acts as the connection between:

```text
User's Cart
      ↓
Selected Product
      ↓
Quantity
```

Later, the same concept will be used when creating:

```text
Order
 ↓
OrderItem
 ↓
Product
```

So understanding `CartItem` is important before starting the order system.

---

# 📚 What I Should Understand After Day 7

- [ ] Foreign keys
- [ ] One-to-many relationships
- [ ] Cart and CartItem design
- [ ] Authentication
- [ ] Authorization
- [ ] User ownership
- [ ] SQLAlchemy queries
- [ ] `.first()`
- [ ] `.all()`
- [ ] Database transactions
- [ ] Stock validation
- [ ] Business logic
- [ ] Pydantic schemas
- [ ] Cart total calculation
- [ ] CRUD operations
- [ ] `ON DELETE CASCADE`

---

# 🚧 What Is Still Left in the Project

## Day 8 — Orders & Checkout

Next major functionality:

- Create Order model
- Create OrderItem model
- Convert cart into order
- Calculate order total
- Store order status
- Store order date
- Connect order with user
- Connect order items with products
- Clear cart after successful order
- Reduce product stock

---

## After Orders

Still remaining:

### 📦 Order Management

- View user's orders
- View individual order
- Cancel order
- Admin order management
- Update order status

### 💳 Payments

- Payment integration
- Payment verification
- Payment status
- Failed payments
- Successful payments

### 🧪 Testing

- User tests
- Authentication tests
- Product tests
- Cart tests
- Order tests
- Payment tests

### 🚀 Production

- Environment variables
- Docker
- PostgreSQL production setup
- CI/CD
- Deployment
- API documentation
- Security improvements

---

# 🎯 Day 7 Summary

Today I built the **Shopping Cart system**.

The important architecture learned today was:

```text
Authenticated User
       ↓
      Cart
       ↓
   Cart Items
       ↓
    Products
       ↓
Price + Quantity + Stock
       ↓
 Business Logic
       ↓
    API Response
```

The cart system is now ready to become the foundation for the next major part of the project:

```text
🛒 Cart
  ↓
📦 Order
  ↓
💳 Payment
  ↓
✅ Purchase
```

## Day 7 Status

**🟢 COMPLETE**

## Next Goal

**Day 8 — Orders & Checkout**
