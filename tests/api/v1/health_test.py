"""Tests for GET /api/v1/health."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_health_returns_200(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.unit
def test_health_status_is_ok(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.json()["status"] == "ok"


@pytest.mark.unit
def test_health_version_is_non_empty_string(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    version = response.json()["version"]
    assert isinstance(version, str)
    assert len(version) > 0
