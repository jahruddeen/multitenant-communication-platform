
# Automated SMS Voice Platform

A multi-company SMS and Voice Notification Platform.

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Docker
- GitHub Actions

## Features

1. Company Registration
2. JWT Login
3. Company-wise Data Isolation
4. Contact Management
5. CSV Upload
6. SMS Notification API
7. Voice Calling API
8. Consent Management
9. Opt-out Functionality
10. Notification Reports
11. Docker Deployment
12. GitHub Actions CI

## Installation

### Create Virtual Environment

python -m venv venv

### Activate Environment

Windows:

venv\Scripts\activate

Linux:

source venv/bin/activate

### Install Dependencies

pip install -r requirements.txt

### Run Application

uvicorn app.main:app --reload

## Swagger Documentation

http://127.0.0.1:8000/docs

## Health Check

http://127.0.0.1:8000/health

## Docker Deployment

docker compose up --build -d

## Run Tests

pytest -q

## GitHub Deployment

git init

git add .

git commit -m "Initial project setup"

git branch -M main

git remote add origin https://github.com/YOUR_USERNAME/automated-sms-voice-platform.git

git push -u origin main

## Safety

The application defaults to mock SMS and voice mode.

Do not enable real communication without documented
recipient consent, appropriate telecom compliance,
provider approval, opt-out handling and rate limits.
