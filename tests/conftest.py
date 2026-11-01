
import os

os.environ["DATABASE_URL"] = "sqlite:///./test_notifications.db"

os.environ["SECRET_KEY"] = "test-secret-key"

os.environ["PROVIDER_MODE"] = "mock"


import pytest

from fastapi.testclient import TestClient

from app.main import app

from app.database import Base, engine


@pytest.fixture()
def client():

    Base.metadata.drop_all(
        bind=engine
    )

    Base.metadata.create_all(
        bind=engine
    )

    with TestClient(app) as test_client:

        yield test_client

    Base.metadata.drop_all(
        bind=engine
    )
