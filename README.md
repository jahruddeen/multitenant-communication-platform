# Multitenant Communication Platform

**An Enterprise-Ready Communication Management Backend built with FastAPI and Python.**

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red.svg)](https://www.sqlalchemy.org/)
[![API](https://img.shields.io/badge/API-REST-orange.svg)](https://fastapi.tiangolo.com/)

## Overview

The **Multitenant Communication Platform** is a backend application designed to manage enterprise communication operations across multiple companies from a centralized platform.

Built with **FastAPI** and **SQLAlchemy**, the system supports company management, user authentication, contact management, SMS notifications, voice call operations, consent tracking, and communication reporting. It is designed to scale cleanly for multi-tenant business environments while remaining easy to extend for future integrations and cloud deployment.

## Project Preview

![Multitenant Communication Platform Dashboard](https://via.placeholder.com/1400x700/0f172a/ffffff?text=Multitenant+Communication+Platform)

This interface showcases the API-driven communication platform for managing authentication, companies, contacts, SMS, voice workflows, and reporting in a single backend system.

## Key Features

### 1. Multi-Tenant Company Management
- Centralized company onboarding and management
- Company-specific user and contact records
- Organization-level isolation and data separation

### 2. Authentication and Authorization
- JWT-based authentication
- Secure password hashing
- Role-based access control
- Company admin authorization checks

### 3. Contact Management
- Create, update, and manage contacts
- Company-specific contact storage
- SMS and voice consent tracking
- Opt-out and consent history management

### 4. SMS Management
- Send and track SMS notifications
- Delivery status tracking
- Provider message ID logging
- Notification and error history

### 5. Voice Call Management
- Voice call request handling
- Retry scheduling support
- Attempt tracking and cooldown checks
- Communication logging

### 6. Consent Management
- SMS consent records
- Voice consent records
- Consent history tracking
- Opt-out status management

### 7. Reporting and Monitoring
- Notification activity logs
- SMS and voice communication summaries
- Status-based reporting
- Company-level insights and monitoring

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Password Security | pwdlib |
| Database | SQLAlchemy-supported database |
| API Documentation | Swagger UI / OpenAPI |
| ASGI Server | Uvicorn |
| Version Control | Git and GitHub |

## Application Architecture

```text
Multitenant Communication Platform
              |
              v
         FastAPI Backend
              |
     +--------+---------+
     |        |         |
     v        v         v
 Authentication Company Contacts
     |        |         |
     +--------+---------+
              |
     +--------+---------+
     |        |         |
     v        v         v
    SMS     Voice     Reports
  Service   Service
     |        |
     +--------+
          |
          v
    Notification Logs
          |
          v
       Database
```

## Project Structure

```text
multitenant-communication-platform/
│
├── app/
│   └── __init__.py
│
├── apps/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── companies.py
│       ├── contacts.py
│       ├── sms.py
│       ├── calls.py
│       └── reports.py
│
├── services/
│   ├── scheduler.py
│   ├── sms_service.py
│   └── voice_service.py
│
├── tests/
│   └── conftest.py
│
├── auth.py
├── config.py
├── models.py
├── schemas.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env.example
```

## Prerequisites

Before running the application, make sure the following are installed:

- Python 3.11 or later
- pip
- Git
- A supported database configured for the project
- Access to required environment variables

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/jahruddeen/multitenant-communication-platform.git
```

### Step 2: Navigate to the Project Directory

```bash
cd multitenant-communication-platform
```

### Step 3: Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If needed for email validation in Pydantic models, install:

```bash
pip install email-validator
```

### Step 5: Configure Environment Variables

Create a `.env` file or use your project environment configuration and set values such as:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./notifications.db
PROVIDER_MODE=mock
APP_NAME=Multitenant Communication Platform
```

Do not commit production secrets or sensitive credentials to GitHub.

### Step 6: Start the Application

Use this command from the project root:

```bash
python -m uvicorn apps.main:app --reload --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/
```

> Note: Do not use `http://0.0.0.0:8000/` in the browser. `0.0.0.0` is the bind address for the server, not the browser URL.

## API Documentation

After starting the application, access the API documentation here:

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI Schema | http://127.0.0.1:8000/openapi.json |

Swagger UI provides a simple way to explore and test the available API endpoints.

## Security Considerations

- Store secrets in environment variables or a secure secrets manager
- Never commit database credentials or JWT signing secrets
- Apply proper role-based authorization to protected endpoints
- Validate consent before sending SMS or initiating voice calls
- Restrict access to company-specific records
- Use HTTPS in production
- Configure database backups and access control policies

## Future Enhancements

The platform can be extended with:

- React-based admin dashboard
- Docker containerization
- Kubernetes and Azure Kubernetes Service (AKS)
- Azure Container Registry (ACR)
- Azure DevOps CI/CD workflows
- Terraform-based infrastructure provisioning
- Prometheus and Grafana monitoring
- Advanced analytics and reporting
- Centralized logging and alerting

## Development

Contributions, improvements, and feature suggestions are welcome.

1. Fork the repository
2. Create a feature branch
3. Implement and test your changes
4. Submit a pull request

## Author

**Jahruddeen Ansari**

GitHub: https://github.com/jahruddeen

Project: [Multitenant Communication Platform](https://github.com/jahruddeen/multitenant-communication-platform)

---

**Built with Python and FastAPI | Designed for Enterprise Communication Management**

