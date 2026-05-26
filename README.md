# Loan Prediction System

A Django-based loan prediction system with machine learning, JWT authentication, and comprehensive loan management.

## Features

- User roles: Applicant, Loan Officer, Credit Analyst, Admin
- Loan application submission with document upload
- ML-based risk prediction (XGBoost/LightGBM)
- SHAP explainability for predictions
- JWT authentication with refresh tokens
- Audit logging
- RESTful API with Swagger docs

## Tech Stack

- Django 5.x
- Django REST Framework
- MySQL 8+
- XGBoost/LightGBM
- Celery + Redis
- Docker

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements/dev.txt`
4. Copy `.env.example` to `.env` and configure
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`

## Docker

```bash
docker-compose up -d
```

## API Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - Login
- `GET /api/auth/profile/` - User profile
- `POST /api/loans/` - Submit loan application
- `POST /api/predict/` - Get prediction
- `GET /api/analytics/dashboard/` - Dashboard stats

## Testing

```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.