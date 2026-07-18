# Payment Gateway Integration
## Gowes Ya

## Objective

Implement a complete production-ready payment gateway integration for the existing Paid Event feature.

The Event module and monetization system already exist.

Do NOT redesign the UI.

Do NOT modify existing event functionality.

Only implement the complete payment process.

---

# Payment Gateway

Use Midtrans as the primary payment gateway.

Architecture must be modular so another provider (Xendit, Stripe, etc.) can be added in the future without changing business logic.

Use a Payment Provider abstraction.

---

# Supported Payment Methods

Implement support for:

- QRIS
- GoPay
- ShopeePay
- Bank Transfer (BCA, BNI, BRI, Mandiri)
- Credit Card
- Debit Card

The available payment methods should be configurable from the Admin Panel.

---

# Payment Flow

Participant

↓

Tap "Register & Pay"

↓

Backend creates Order

↓

Calculate:

- Ticket Price
- Platform Service Fee
- Total Amount

↓

Generate Midtrans Transaction

↓

Receive Snap Token / Redirect URL

↓

Frontend opens Midtrans Payment Page

↓

Participant completes payment

↓

Midtrans sends Callback

↓

Backend verifies signature

↓

Update payment status

↓

Generate Event Ticket

↓

Register participant

↓

Send confirmation notification

↓

Update organizer dashboard

---

# Payment Status

Support all statuses:

Pending

Capture

Settlement

Success

Expire

Cancel

Refund

Chargeback

Failed

The frontend must update automatically after every status change.

---

# Backend Requirements

Implement:

Payment Service

Payment Provider Interface

Midtrans Provider

Webhook Controller

Payment Verification Service

Receipt Generator

Invoice Generator

Refund Service

---

# Webhook

Implement secure webhook verification.

Validate:

Server Key Signature

Order ID

Transaction ID

Gross Amount

Payment Status

Reject invalid requests.

Never trust client-side payment confirmation.

Only webhook updates payment status.

---

# Orders

Each payment creates:

Unique Order Number

Transaction ID

Invoice Number

Receipt Number

Payment History

Audit Log

---

# Database

Create or extend tables:

payments

payment_transactions

payment_logs

payment_callbacks

receipts

invoices

refund_requests

payment_methods

---

# Organizer Revenue

Automatically calculate:

Ticket Revenue

Platform Fee

Net Revenue

Pending Revenue

Paid Revenue

Refunded Revenue

---

# Receipts

Generate digital receipts.

Include:

Order Number

Event Name

Participant Name

Ticket Price

Platform Fee

Total Payment

Payment Method

Payment Date

Transaction ID

Payment Status

Organizer

Receipt Number

Receipts should be downloadable as PDF.

---

# Refund

Support refund requests.

Workflow:

Participant requests refund

↓

Organizer/Admin reviews

↓

Approve or Reject

↓

If approved

↓

Trigger Midtrans Refund API

↓

Update payment

↓

Update participant status

↓

Update revenue

↓

Send notification

---

# Notifications

Notify participant when:

Payment Created

Payment Pending

Payment Successful

Payment Failed

Payment Expired

Ticket Generated

Refund Approved

Refund Rejected

Notify organizer when:

New Paid Registration

Payment Successful

Refund Request

Refund Completed

---

# Security

Never expose Server Key.

Store API keys securely.

Validate all callbacks.

Prevent duplicate callbacks.

Prevent duplicate payments.

Prevent duplicate registrations.

Protect against replay attacks.

Log every payment event.

---

# Admin

Admin can:

View all transactions

Search payments

Filter by status

Refund payments

Configure payment methods

Configure platform fee

View payment analytics

Export transaction reports

---

# Acceptance Criteria

Implementation is complete only if:

✓ Participant can pay using Midtrans.

✓ QRIS works.

✓ GoPay works.

✓ Bank Transfer works.

✓ Payment status updates automatically.

✓ Webhook verification is secure.

✓ Ticket is generated only after successful payment.

✓ Organizer revenue is calculated correctly.

✓ Platform service fee is calculated correctly.

✓ Receipts are generated.

✓ Refunds work correctly.

✓ Notifications are sent automatically.

✓ No mock payment.

✓ No placeholder implementation.

✓ Production-ready implementation.

Continue implementing until the complete payment workflow functions end-to-end with the existing Gowes Ya application.
