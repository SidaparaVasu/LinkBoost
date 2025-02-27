# Referral System Backend (Django)

A simple referral system built using Django and Django REST Framework (DRF). This system allows users to register using referral links, track their referrals, and view referral statistics.

## Features

- User registration & login with referral tracking
- Referral link generation
- Referral statistics (total & successful referrals)
- JWT authentication
- Session-based login/logout

## Installation

### Prerequisites

Ensure you have the following installed:

- Follow requirements.txt file

### Setup

1. **Clone the repository**

```bash
    git clone https://github.com/SidaparaVasu/LinkBoost
```

2. **Create a virtual environment & activate it**

```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies**

```bash
    pip install -r requirements.txt
```

4. \*\*Navigate to Project directory

```
    cd LinkBoost
```

5. **Run migrations**

```bash
    python manage.py makemigrations
    python manage.py migrate
```

6. **Create a superuser (optional)**

```bash
    python manage.py createsuperuser
```

7. **Start the development server**

```bash
    python manage.py runserver
```

## API Endpoints

### Authentication

- `POST /api/register/` → Register a new user
- `POST /api/login/` → Login with email & password
- `GET /api/logout/` → Logout the user

### Referral System

- `GET /api/referrals/` → Get the authenticated user's referral code & link
- `GET /api/referral-stats/` → Get referral statistics (total & successful referrals)

## Usage

### Generating Referral Links

Once logged in, users can share their referral link, which looks like:

```
http://127.0.0.1:8000/register?referral=<referral_code>
```

When a new user registers using this link, their account will be linked to the referrer.

### Tracking Referrals

On the user dashboard, referred users and their referral statuses (pending/successful) are displayed.

## Technologies Used

- **Django** - Backend framework
- **Django REST Framework (DRF)** - API development
- **SQLite3** - Default database (can be changed to PostgreSQL)

## Developed by _Vasu Sidapara_ with ❤️.
