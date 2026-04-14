"""Smoke tests for the application entry point."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_app_health_smoke(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
