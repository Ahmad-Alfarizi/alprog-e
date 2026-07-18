# Event Monetization Module
## Gowes Ya

## Objective
Implement a complete monetization system for the existing Event feature in the **Gowes Ya** platform. 

*   **No UI Redesign:** The Event module already exists and is fully functional. Do NOT redesign any core UI elements.
*   **No Functionality Removal:** Do NOT remove or deprecate any existing functionality.
*   **Extension-Based Approach:** Extend the current implementation by adding seamless support for both **Free Events** and **Paid Events**.
*   **Monetization Engine:** The monetization model must strictly use a **Service Fee** model charged to the participant.

---

# Business Model
The platform categorizes events into two distinct structural types, each dictating a specific participant onboarding lifecycle:

### Free Event
*   Participants can join immediately upon clicking the registration button.
*   No payment transaction or gateway redirection is required.
*   **State Transition:** Clicking "Join" instantly moves the participant's enrollment status to: `Registered`.

### Paid Event
*   Participants must successfully complete the financial transaction before their registration is validated and slots are officially locked.
*   **Workflow:**
    $$	ext{Join Event} \longrightarrow 	ext{Payment Process} \longrightarrow 	ext{Payment Success} \longrightarrow 	ext{Registration Confirmed} \longrightarrow 	ext{Digital Ticket Generated}$$

---

# Service Fee
To maximize platform growth and maintain organizer loyalty, the platform adheres to a zero-cost creation model for organizers:
*   **Organizer Policy:** The organizer should **NEVER** pay to create an event. Creating events is always **FREE**.
*   **Platform Revenue Model:** The platform earns its revenue by charging participants a configurable **Service Fee** on top of the base ticket price at the time of purchase.

### Financial Split Example
*   **Ticket Base Price:** Rp50.000
*   **Platform Service Fee:** Rp2.500
*   **Participant Total Gross Payment:** **Rp52.500**

#### Revenue Distribution Execution:
*   **Organizer receives:** Rp50.000 (100% of base ticket price)
*   **Platform receives:** Rp2.500 (100% of platform service fee)

### Configuration Rules
The Service Fee engine must be fully dynamic and manageable via the Admin Panel. It must support the following calculation strategies:
1.  **Fixed Amount:** A constant nominal amount per ticket (e.g., Rp2.500 flat fee per registration).
2.  **Percentage:** A variable fee based on the ticket price (e.g., 5% of the ticket base price).
3.  **Future Promotions:** Tiered fee architectures, fee caps, or temporary waivers for promotional cycles.

---

# Create Event
Extend the existing `Create Event` form field validation schema and UI template. Add the following input parameters:

*   **Event Type Input Selector:**
    *   `○ Free Event` (Radio / Select Option)
    *   `○ Paid Event` (Radio / Select Option)

### Conditional Field Rendering Logic:
*   **If `Paid Event` is selected, dynamically expose and validate the following fields:**
    *   `Ticket Price`: Numeric input field (Must be greater than 0, formatted with currency controls).
    *   `Currency`: Dropdown selector (Defaults to IDR).
    *   `Registration Deadline`: Datetime picker (Must be set prior to the actual Event start date).
    *   `Refund Policy`: Rich text editor / Toggle template select (Optional field).
*   **If `Free Event` is selected:**
    *   Hide all payment-related fields completely.
    *   Set `Ticket Price` to 0 automatically within the payload data structure.

---

# Event Card
Enhance the existing summary Event Cards used across discovery grids, search results, and recommendations:
*   **Badge Implementation:** Overlay a small, highly readable UI badge on the card element.
*   **Visual States:**
    *   `FREE`: Displayed using a subtle green or neutral accent background.
    *   `PAID`: Displayed using a professional dark blue, slate, or brand accent background.
*   **Constraint:** Do not alter the core sizing, grid layout, image dimensions, or informational typography of the existing event card. Only append the specified structural badge.

---

# Event Detail
The `Event Detail` presentation page dynamically shifts its call-to-action (CTA) module and pricing summary block based on the underlying event metadata:

### Case A: If Free Event
*   **Rendered Action:** A highly visible `Join Event` button. Clicking triggers immediate registration without moving to a checkout flow.

### Case B: If Paid Event
*   **Rendered Information Breakdown Matrix:**
    *   **Ticket Price:** Displays base cost set by the organizer (e.g., `Rp50.000`).
    *   **Platform Fee:** Displays calculated live service fee from the configuration engine (e.g., `Rp2.500`).
    *   **Total Payment:** Bold calculation block combining base and fee (e.g., `Rp52.500`).
*   **Rendered Action:** A clear `Register & Pay` CTA button that initiates an order session and locks the user's intent to pay.

---

# Registration Flow

### Free Event Flow Chart
```
[User Taps "Join"] 
        ↓
[API Validates Available Slots] 
        ↓
[Database Insert: Registration Record State = 'Registered']
        ↓
[Render Success View & Send Email Confirmation]
```

### Paid Event Flow Chart
```
[User Taps "Register & Pay"] 
        ↓
[API Creates Order & Calculates Live Platform Service Fees] 
        ↓
[Initialize Transaction with Integrated Payment Gateway Provider] 
        ↓
[User Redirected to Payment Gateway Gateway UI / Secure Element] 
        ↓
[Asynchronous Webhook Callback: Payment Success Confirmed] 
        ↓
[State Update: Order = 'Paid', Registration = 'Confirmed'] 
        ↓
[Generate Crypto-Signed QR Digital Ticket & Invoice PDF]
```

---

# Payment Status
The billing ledger engine strictly adheres to a finite state machine architecture to manage orders throughout their transaction life-cycle:

| Status State | Definition & Trigger Event |
| :--- | :--- |
| **Pending** | Initial state when order is generated; awaiting user checkout validation or bank transfer confirmation. |
| **Paid** | Successful receipt of funds confirmed via secure asynchronous payment gateway API webhook callback. |
| **Expired** | The user failed to complete payment within the specified transaction timeout limit (e.g., 2 hours). Slots are automatically released. |
| **Cancelled**| Manual termination of the payment intention by the participant prior to processing or execution. |
| **Refunded** | Funds returned partially or fully to the participant following a valid cancel/refund request approved by policies. |
| **Failed** | Systemic or transactional rejection by the payment processor gateway (e.g., insufficient balances, bad credentials). |

---

# Organizer Dashboard
Extend the analytical metrics grid inside the Event Organizer Console to track real-time revenue performance metrics. 

### Metrics Matrices
*   **Total Ticket Sales:** Cumulative count of paid digital tickets issued ($N_{	ext{tickets}}$).
*   **Total Revenue:** Gross cash inflow collected from customers including platform service fees ($\sum 	ext{Total Paid}$).
*   **Platform Fee:** Total accrued monetization cut transferred to platform account balances ($\sum 	ext{Service Fee}$).
*   **Net Revenue:** Net balance distributable directly to the organizer ($	ext{Total Revenue} - 	ext{Platform Fee}$).
*   **Participants:** Total count of active, confirmed registrants across both Free and Paid criteria.
*   **Remaining Slots:** Live calculation of capacity limit subtraction ($	ext{Max Capacity} - 	ext{Confirmed Registrants}$).
*   **Pending Payments:** Count and prospective monetary value of orders currently trapped in the `Pending` state machine.
*   **Completed Payments:** Count and monetary breakdown of transactions marked as `Paid`.

---

# Participant Features
Provide the following self-service capabilities to registered users through their personal event booking dashboard:

1.  **View Ticket:** Access digital passes featuring encrypted high-density QR/Barcodes containing validation payloads (`ticket_uuid`, `user_id`, `event_id`).
2.  **View Payment Status:** Real-time visibility into whether their order sits at pending, failed, or completed benchmarks.
3.  **Download Receipt:** Production-ready PDF document rendering confirming clear split-breakdown invoices.
4.  **Cancel Registration:** Allows exit loops from an event if executed **before** the registration deadline threshold passes.
5.  **Request Refund:** Accessible for paid tickets only if the organizer explicitly toggled the refund availability configuration on event creation.

---

# Admin Configurations
The central platform administrator panel must provide explicit functional controls to alter parameters globally or per category:

*   **Platform Service Fee Controls:** Adjust global calculation variables (Toggle between flat fixed IDR rate, specific percentage multiplier, or custom discount parameters).
*   **Supported Payment Methods:** Central control switches to enable/disable transactional rails (e.g., Virtual Accounts, E-Wallets like OVO/Gopay, Credit Card matrices, QRIS).
*   **Refund Rules Configuration:** Establish global threshold matrices (e.g., maximum refund execution window like $X$ days prior to event kickoff).
*   **Tax Rules Engine:** Incorporate regional VAT/PPN computations directly into invoicing where applicable.
*   **Promotional Engine Management:**
    *   **Promotional Discounts:** Global service fee waivers for seasonal periods.
    *   **Coupon Codes:** System to generate custom alphanumeric code strings enabling participants to minimize ticket price or waive service fees.

---

# Database Schema Architecture
Extend the existing relational structure by deploying the following schema models. Foreign keys must maintain high relational integrity constraints.

### 1. `ServiceFees`
Tracks history and current configurations of service fees applied to transactions.
*   `id` (UUID, Primary Key)
*   `fee_type` (Enum: 'FIXED', 'PERCENTAGE')
*   `fee_value` (Decimal(12,2))
*   `is_active` (Boolean)
*   `created_at` / `updated_at` (Timestamp)

### 2. `Coupons`
Stores promotional discount keys.
*   `id` (UUID, Primary Key)
*   `code` (Varchar, Unique Index)
*   `discount_type` (Enum: 'PERCENTAGE', 'FIXED_AMOUNT')
*   `discount_value` (Decimal(12,2))
*   `max_uses` / `used_count` (Integer)
*   `expiry_date` (Timestamp)

### 3. `EventOrders`
Primary order records combining user, event, and discount references.
*   `id` (UUID, Primary Key)
*   `order_number` (Varchar, Unique)
*   `user_id` (UUID, FK to Users)
*   `event_id` (UUID, FK to Events)
*   `coupon_id` (UUID, FK to Coupons, Nullable)
*   `base_amount` (Decimal(12,2))
*   `fee_amount` (Decimal(12,2))
*   `discount_amount` (Decimal(12,2))
*   `total_amount` (Decimal(12,2))
*   `status` (Enum: 'PENDING', 'PAID', 'EXPIRED', 'CANCELLED', 'REFUNDED', 'FAILED')
*   `created_at` / `updated_at` (Timestamp)

### 4. `Payments`
Core billing engine integration records mapping to gateway providers.
*   `id` (UUID, Primary Key)
*   `order_id` (UUID, FK to EventOrders)
*   `transaction_reference` (Varchar, External Gateway ID)
*   `payment_method_id` (UUID, FK to PaymentMethods)
*   `amount_paid` (Decimal(12,2))
*   `payment_status` (Varchar)
*   `paid_at` (Timestamp, Nullable)

### 5. `PaymentMethods`
Maintains records of active payment channels.
*   `id` (UUID, Primary Key)
*   `provider_name` (Varchar - e.g., 'Midtrans', 'Xendit')
*   `method_type` (Varchar - e.g., 'QRIS', 'VA_MANDIRI')
*   `is_enabled` (Boolean)

### 6. `Transactions`
Double-entry ledger mapping revenue splits accurately.
*   `id` (UUID, Primary Key)
*   `order_id` (UUID, FK to EventOrders)
*   `organizer_share` (Decimal(12,2))
*   `platform_share` (Decimal(12,2))
*   `payout_status` (Enum: 'HELD', 'SETTLED', 'REFUNDED')

### 7. `Refunds`
Tracks ledger adjustments for reversals.
*   `id` (UUID, Primary Key)
*   `order_id` (UUID, FK to EventOrders)
*   `refund_reason` (Text)
*   `refund_amount` (Decimal(12,2))
*   `status` (Enum: 'REQUESTED', 'APPROVED', 'REJECTED')
*   `processed_at` (Timestamp, Nullable)

### 8. `Receipts`
Stores invoice metadata links.
*   `id` (UUID, Primary Key)
*   `order_id` (UUID, FK to EventOrders)
*   `receipt_number` (Varchar, Unique Index)
*   `pdf_storage_url` (Varchar)
*   `generated_at` (Timestamp)

### 9. `PaymentLogs`
Audit logs for diagnostic debugging.
*   `id` (BigInt, Primary Key)
*   `order_id` (UUID, Nullable)
*   `payload_direction` (Enum: 'INBOUND', 'OUTBOUND')
*   `raw_payload` (JSONB)
*   `timestamp` (Timestamp)

---

# API Specifications

### 1. Calculate Fee
*   **Endpoint:** `POST /api/v1/orders/calculate-fee`
*   **Payload Request:**
    ```json
    {
      "event_id": "8c7b8e1a-4d32-4d7a-8d1b-8e2b3c4d5e6f",
      "coupon_code": "GOWESMERDEKA"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "base_price": 50000.00,
      "service_fee": 2500.00,
      "discount_amount": 5000.00,
      "total_payment": 47500.00,
      "currency": "IDR"
    }
    ```

### 2. Create Order
*   **Endpoint:** `POST /api/v1/orders/create`
*   **Payload Request:**
    ```json
    {
      "event_id": "8c7b8e1a-4d32-4d7a-8d1b-8e2b3c4d5e6f",
      "coupon_code": "GOWESMERDEKA"
    }
    ```
*   **Response (201 Created):**
    ```json
    {
      "order_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "order_number": "ORD-20260718-99481",
      "status": "PENDING",
      "total_amount": 47500.00
    }
    ```

### 3. Initiate Payment
*   **Endpoint:** `POST /api/v1/payments/initiate`
*   **Payload Request:**
    ```json
    {
      "order_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "payment_method_id": "4a5b6c7d-8e9f-0a1b-2c3d-4e5f6a7b8c9d"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "payment_id": "p9o8i7u6-y5t4-r3e2-w1q0-m9n8b7v6c5x4",
      "gateway_redirect_url": "https://checkout.paymentgateway.com/v1/charge/token_id_9921",
      "token": "snap_token_xyz123abc",
      "expiry_time": "2026-07-18T23:59:59Z"
    }
    ```

### 4. Payment Callback (Webhook Entry point)
*   **Endpoint:** `POST /api/v1/payments/callback`
*   **Security Header:** `X-Gateway-Signature: sha256_hash_string`
*   **Payload Request:**
    ```json
    {
      "transaction_id": "ext-txn-88192019A",
      "order_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "gross_amount": "47500.00",
      "payment_status": "settlement",
      "signature_key": "verified_hash_match"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "status": "SUCCESS",
      "message": "Callback processed completely, ledger aligned."
    }
    ```

### 5. Verify Payment
*   **Endpoint:** `GET /api/v1/payments/verify/{order_id}`
*   **Response (200 OK):**
    ```json
    {
      "order_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "status": "PAID",
      "verified_at": "2026-07-18T22:15:30Z"
    }
    ```

### 6. Generate Ticket
*   **Endpoint:** `POST /api/v1/tickets/generate`
*   **Payload Request:**
    ```json
    {
      "order_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "ticket_id": "t1i2c3k4-e5f6-7a8b-9c0d-ticketuuid99",
      "secure_qr_payload": "GOWESYA-SECURE-VALIDATION-TOKEN-STRING",
      "download_url": "https://storage.gowesya.com/tickets/t1i2c3k4.pdf"
    }
    ```

### 7. Refund Request
*   **Endpoint:** `POST /api/v1/refunds/request`
*   **Payload Request:**
    ```json
    {
      "order_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "reason": "Health emergency, cannot attend the ride."
    }
    ```
*   **Response (202 Accepted):**
    ```json
    {
      "refund_id": "r1e2f3u4-n5d6-7a8b-9c0d-refunduuid88",
      "status": "REQUESTED"
    }
    ```

### 8. Organizer Revenue Metrics
*   **Endpoint:** `GET /api/v1/organizer/dashboard/revenue?event_id={event_id}`
*   **Response (200 OK):**
    ```json
    {
      "event_id": "8c7b8e1a-4d32-4d7a-8d1b-8e2b3c4d5e6f",
      "total_ticket_sales": 120,
      "total_gross_revenue": 6300000.00,
      "platform_fee_retained": 300000.00,
      "net_organizer_payout": 6000000.00,
      "pending_payments_count": 5
    }
    ```

### 9. Admin Fee Settings
*   **Endpoint:** `PUT /api/v1/admin/settings/fee`
*   **Payload Request:**
    ```json
    {
      "fee_type": "PERCENTAGE",
      "fee_value": 5.00,
      "apply_globally": true
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "status": "UPDATED",
      "current_policy_id": "fee-policy-uuid-771"
    }
    ```

---

# Notifications Trigger Engine
Automated message routing events are configured to fire via transactional event brokers (e.g., Kafka / RabbitMQ signals) targeting Email, SMS, and Push notification microservices:

1.  **Registration Created:** Emitted immediately when a `Free Event` is joined or a `Paid Event` order is created.
2.  **Payment Pending:** Triggers a push notification detailing payment step instructions and instructions for bank transfers or e-wallet settlement.
3.  **Payment Success:** Delivers an order receipt confirmation email summary outlining the split itemization.
4.  **Payment Failed:** Alerts the user that their slot reservation could not be guaranteed due to an issue with the processor.
5.  **Ticket Generated:** Issues a secure high-density QR asset to the mobile app layout and sends a copy via PDF attachment.
6.  **Refund Approved:** Notifies the participant that their reversal transaction has passed validation checks. The timeline for bank clearings is displayed.
7.  **Refund Rejected:** Sent if a refund request breaks policy criteria (e.g., initiated after the cutoff timeline).
8.  **Event Reminder:** Standard system push notification executed 24 hours prior to standard event flag timings.

---

# Security Matrix & Fraud Safeguards

*   **Payment Callback Verification:** The callback webhook endpoint MUST calculate an HMAC signature based on a shared secret key and compare it directly to the inbound `X-Gateway-Signature` header parameter. Requests failing verification are dropped with `403 Forbidden` statuses.
*   **Race Conditions & Double Payments Prevention:** 
    *   Implement Redis distributed locks on the `{order_id}` key string throughout checkout generation phases.
    *   Enforce strong unique structural database indexes on `Payment(transaction_reference)`.
*   **Double Registration Prevention:** Enforce a composite unique constraint index across `EventOrders(user_id, event_id)` where `status` is inside the state array `['PENDING', 'PAID']`. This makes it structurally impossible for a cyclist to order or register for the exact same event multiple times.
*   **Ticket Ownership Validation:** The generated QR payload must be dynamically signed using asymmetric cryptography keys (RS256). Handheld scanner hardware apps used by field personnel parse the public key component to confirm valid authorization tags.
*   **Secure Organizer Payout Isolation:** Organizer payout accounting maps to segregated ledger records (`Transactions`). Funds remain locked inside a platform escrow settlement account until the event successfully passes validation benchmarks without dispute flags.
*   **Anti-Fraud Rate Limiting:** Apply stringent token bucket rate-limiting thresholds directly to transaction endpoints (`/orders/create` and `/payments/initiate`) to safeguard against denial-of-service attempts.

---

# Acceptance Criteria
The monetization implementation is complete, production-ready, and operational only if all verified operational boxes pass standard validation:

*   [x] **Organizers can successfully create Free Events** using standard entry configurations.
*   [x] **Organizers can successfully create Paid Events** with custom pricing metadata.
*   [x] **Organizers never pay platform fees** for hosting or designing event entries.
*   [x] **Participants pay the baseline ticket cost plus the platform Service Fee** transparently combined.
*   [x] **Revenue distribution split logic acts accurately** on database tables inside double-entry ledger boundaries.
*   [x] **Orders are persistently stored** under accurate relational data rules (`EventOrders`).
*   [x] **Payment instances are tracked explicitly** matching internal logs against gateway transactions (`Payments`).
*   [x] **Crypto-signed Digital Tickets are compiled dynamically** following confirmation states.
*   [x] **Payment callback webhooks are cryptographically validated** to block external manipulation vectors.
*   [x] **Organizer dashboard metrics modules output math equations accurately** reflecting completed payments.
*   [x] **Platform revenue calculations process automatically** on every transaction depending on rules metrics.
*   [x] **Admin users can modify global Platform Service Fee rules** interactively with zero codebase restarts.
*   [x] **Existing Event features remain operational** and free from code regression behavior.
*   [x] **Zero mock data configurations** are left active in the live repository tree.
*   [x] **Zero placeholder logic statements** exist inside the production build profiles.
