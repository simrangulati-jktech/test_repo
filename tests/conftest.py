"""Shared fixtures. Clears the in-memory store around every test."""

import pytest
from fastapi.testclient import TestClient

from app import services
from app.main import app


@pytest.fixture(autouse=True)
def clean_store():
    services.reset()
    yield
    services.reset()


@pytest.fixture
def client():
    return TestClient(app)
