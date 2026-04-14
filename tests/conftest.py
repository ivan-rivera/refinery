"""Shared pytest fixtures."""

import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Return a TestClient wrapping the FastAPI app."""
    return TestClient(app)
