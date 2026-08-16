# E-Commerce Backend API

A production-oriented e-commerce backend built with FastAPI, PostgreSQL, SQLAlchemy, JWT authentication, role-based authorization, cart, orders, admin dashboard, payments, and Razorpay integration.

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT Authentication
- Passlib / bcrypt
- Razorpay
- Docker
- Pytest

---

# Current Progress

## Completed

- User registration and authentication
- JWT authorization
- Role-based access control
- Product CRUD
- Cart system
- Checkout and order creation
- Order history
- Order status management
- Order cancellation
- Stock restoration
- Admin user management
- Admin order management
- Admin dashboard
- Internal payment system
- Razorpay Test Mode integration
- Razorpay payment verification
- Razorpay webhook integration

---

# Day 13 — Razorpay Payment Gateway Integration

## Goal

Integrate a real payment gateway with the existing payment and order system using Razorpay Test Mode.

---

## What Was Completed

### Razorpay SDK Setup

Installed and configured the Razorpay Python SDK.

Created a reusable Razorpay client using environment variables:

- Razorpay Key ID
- Razorpay Key Secret
- Razorpay Webhook Secret

Sensitive credentials are stored in `.env` and loaded through Pydantic Settings.

---

## Razorpay Order Creation

Created an endpoint that generates a Razorpay order for an existing e-commerce order.

Flow:

Customer Order
↓
Validate Order
↓
Check User Ownership
↓
Check Duplicate Payment
↓
Convert Rupees to Paise
↓
Create Razorpay Order
↓
Create Pending Payment Record
↓
Save Razorpay Order ID

The database stores:

- Internal order ID
- Amount
- Payment status
- Payment method
- Razorpay order ID
- Transaction ID

---

## Amount Conversion

The application stores money in rupees.

Razorpay expects the payment amount in the smallest currency unit.

Example:

₹500
↓
50000 paise

Formula:

amount_in_paise = amount_in_rupees × 100

---

## Test Razorpay Checkout

Created a temporary HTML test page to open Razorpay Checkout.

The page uses:

- Razorpay Key ID
- Razorpay Order ID
- Amount in paise

The Razorpay Key Secret is never exposed to the browser.

---

## Payment Signature Verification

Created a backend verification endpoint.

After successful Razorpay Checkout, the frontend receives:

- razorpay_payment_id
- razorpay_order_id
- razorpay_signature

The backend verifies the Razorpay signature before marking the payment successful.

After successful verification:

Payment status → successful

Transaction ID → Razorpay payment ID

Order status → processing

---

# Razorpay Webhooks

A webhook was added so Razorpay can directly notify the FastAPI backend about payment events.

Public webhook access was created using zrok because Razorpay cannot directly access localhost.

Flow:

Razorpay
↓
Public zrok URL
↓
FastAPI Webhook Endpoint
↓
Verify Webhook Signature
↓
Process Event
↓
Update Database

---

## Webhook Security

Webhook requests are verified using:

X-Razorpay-Signature

The signature is validated using a separate:

RAZORPAY_WEBHOOK_SECRET

The raw HTTP request body is verified before parsing the JSON payload.

Unverified webhook requests are rejected.

---

## payment.captured Event

The webhook currently handles successful captured payments.

Flow:

payment.captured
↓
Extract Razorpay Order ID
↓
Find Payment Record
↓
Prevent Duplicate Processing
↓
Payment → successful
↓
Save Razorpay Payment ID
↓
Order → processing

---

## Idempotency

Webhook providers may send the same event multiple times.

The backend checks whether the payment has already been processed before applying the update again.

Example:

if payment already successful
↓
Do not process again

This prevents duplicate side effects.

---

## payment.failed Event

Logic was also prepared for failed payments.

Flow:

payment.failed
↓
Find Payment
↓
Payment → failed
↓
Save Razorpay Payment ID
↓
Order remains pending

A failed payment should not move the order into processing.

---

# Testing Completed

The complete Razorpay Test Mode flow was tested successfully.

Confirmed:

- Razorpay order creation works
- Razorpay Checkout popup opens
- Test payment works
- Razorpay webhook reaches FastAPI
- Webhook signature verification works
- Payment status updates correctly
- Razorpay transaction ID is stored
- Order status changes to processing
- Duplicate payment protection works
- Duplicate webhook protection works

Example webhook response:

POST /payments/webhook → 200 OK

---

# Problems Solved Today

## Webhook Returned 405

Initial Razorpay webhook requests were reaching:

POST /

instead of:

POST /payments/webhook

The webhook URL was corrected by adding the complete endpoint path to the public zrok URL.

After correction:

POST /payments/webhook → 200 OK

---

## Duplicate Payment

An order that already had a payment returned:

409 Conflict

This confirmed that duplicate payment protection was working correctly.

---

# Important Architecture Learned

Order and Payment are separate entities.

Order represents:

WHAT the customer purchased.

Payment represents:

HOW the customer paid.

Current flow:

User
↓
Cart
↓
Order
↓
Payment
↓
Razorpay
↓
Webhook
↓
Payment Successful
↓
Order Processing

---

# Current Limitation

The current database design allows only one payment record per order.

This creates a problem when a payment fails.

Example:

Order
↓
Payment Attempt 1 → failed
↓
Customer wants to retry
↓
Duplicate payment restriction

This will be fixed next by changing:

Order → Payment

from one-to-one to:

Order → Payments

one-to-many.

---

# Next Goal

## Payment Retry Architecture

Planned changes:

- Remove unique constraint from payment.order_id
- Change Order → Payment relationship to one-to-many
- Allow multiple failed payment attempts
- Block a new payment when an active/successful payment already exists
- Test payment retries

After that:

- Razorpay refund integration
- Refund webhook handling
- Stock restoration
- Search and filtering
- Reviews and ratings
- Wishlist
- Coupons
- Automated testing
- Security cleanup
- Docker
- Deployment

---

# Day 13 Status

Razorpay Core Integration: COMPLETE ✅

Webhook Integration: COMPLETE ✅

Successful Payment Flow: COMPLETE ✅

Failed Payment Event Logic: STARTED 🟡

Payment Retry Architecture: NEXT ⏳

Refund Integration: NOT STARTED ⏳
