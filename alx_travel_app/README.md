# ALX Travel App - Django with Chapa Payment Integration

This is a travel application built using Django that allows users to browse listings, make bookings, and process payments through the Chapa payment gateway.

## Features

- User authentication and authorization
- Browse and search travel listings
- Create and manage bookings
- Integrated Chapa payment gateway
- Payment verification and status tracking
- Review and rating system

## Prerequisites

- Python 3.8+
- pip
- PostgreSQL/SQLite (default)
- Chapa API account

## Setting Up the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd alx-travel-app
```
### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables
Create a `.env` file in the project root and add the following variables:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (Optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/alx_travel_db

# Chapa API Configuration
CHAPA_SECRET_KEY=your-chapa-secret-key
CHAPA_PUBLIC_KEY=your-chapa-public-key

# Email Configuration (for payment confirmations)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```
### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Setup and Seed Database

```bash
python manage.py setup_db --seed
```
### 7. Create a Superuser

```bash
python manage.py createsuperuser
```
### 8. Run the Development Server
```bash
python manage.py runserver
```

## API Endpoints
### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login user and obtain JWT token
- `POST /api/auth/logout/` - Logout user

### Listings
- `GET /api/listings/` - Retrieve all listings
- `GET /api/listings/<id>/` - Retrieve a specific listing
- `POST /api/listings/` - Create a new listing (authenticated)
- `PUT /api/listings/<id>/` - Update a listing (authenticated)
- `DELETE /api/listings/<id>/` - Delete a listing (authenticated)

### Bookings
- `POST /api/bookings/` - Create a new booking (authenticated)
- `GET /api/bookings/<id>/` - Retrieve a specific booking (authenticated)
- `GET /api/bookings/user/` - Retrieve bookings for the logged-in user (authenticated)
- `PUT /api/bookings/<id>/` - Update a booking (authenticated)
- `DELETE /api/bookings/<id>/` - Cancel a booking (authenticated)

### Payments
- `POST /api/payments/initiate/` - Initiate a payment (authenticated)
```json
{
  "booking_id": "uuid",
  "return_url": "http://yourapp.com/success"
}

```
- `GET /api/payments/verify/?tx_ref=BK-{booking_id}` - Verify payment status (authenticated)
- `GET /api/payments/` - Retrieve payment history for the logged-in user (authenticated)
- `GET /api/payments/<id>/` - Retrieve a specific payment (authenticated)

## Payment Workflow
1. User creates a booking via the `/api/bookings/` endpoint.
```json
{
  "listing_id": "uuid",
  "check_in_date": "2024-01-15",
  "check_out_date": "2024-01-20"
}
```
2. User initiates payment via the `/api/payments/initiate/` endpoint.
```json
{
  "booking_id": "booking-uuid",
  "return_url": "http://localhost:8000/payment/success"
}
```
### Response
```json
{
  "payment_url": "https://checkout.chapa.co/checkout/payment/...",
  "reference": "BK-booking-uuid",
  "status": "success"
}
```
3. User is redirected to Chapa's payment page to complete the transaction.
4. After payment, Chapa redirects the user to the specified return URL.
5. The application verifies the payment status via the `/api/payments/verify/` endpoint.
```http
GET /api/payments/verify/?tx_ref=BK-booking-uuid
```
### Response
```json
{
  "reference": "BK-booking-uuid",
  "status": "completed",
  "amount": "5000.00"
}
```

## Project Structure
```
alx_travel_app/
├── alx_travel_app/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── listings/
│   ├── models.py          # Listing, Booking, Payment, Review models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # ViewSets and API endpoints
│   ├── urls.py            # URL routing
│   └── tests.py           # Unit tests
├── manage.py
├── requirement.txt
├── .env
└── README.md
```