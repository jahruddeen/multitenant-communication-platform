from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from config import settings

from apps.database import Base, engine

from apps.routers import (
    auth,
    companies,
    contacts,
    sms,
    calls,
    reports
)


# CREATE DATABASE TABLES

Base.metadata.create_all(
    bind=engine
)


# FASTAPI APPLICATION

app = FastAPI(

    title=settings.APP_NAME,

    description="Multi Company SMS and Voice Notification Platform",

    version="1.0.0"
)


# CORS CONFIGURATION

origins = (
    ["*"]
    if settings.ALLOWED_ORIGINS == "*"
    else settings.ALLOWED_ORIGINS.split(",")
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=[
        "GET",
        "POST",
        "PATCH",
        "DELETE"
    ],

    allow_headers=[
        "Authorization",
        "Content-Type"
    ]
)


# REGISTER API ROUTERS

app.include_router(auth.router)

app.include_router(companies.router)

app.include_router(contacts.router)

app.include_router(sms.router)

app.include_router(calls.router)

app.include_router(reports.router)


# ROOT API

@app.get("/")
def root():

    return {

        "application": settings.APP_NAME,

        "status": "running",

        "provider_mode": settings.PROVIDER_MODE

    }


# HEALTH CHECK

@app.get("/health")
def health():

    return {

        "status": "healthy"

    } 