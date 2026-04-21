import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with patch('redis.Redis') as mock_redis:
    mock_redis.return_value = MagicMock()
    from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis():
    with patch('main.r') as mock_r:
        mock_r.lpush = MagicMock(return_value=1)
        mock_r.hset = MagicMock(return_value=1)
        mock_r.hget = MagicMock(return_value="queued")
        yield mock_r

def test_create_job(mock_redis):
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) > 0

def test_get_job_found(mock_redis):
    mock_redis.hget.return_value = "completed"
    response = client.get("/jobs/test-job-123")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-123"
    assert data["status"] == "completed"

def test_get_job_not_found(mock_redis):
    mock_redis.hget.return_value = None
    response = client.get("/jobs/nonexistent-job")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "not found"

def test_create_job_pushes_to_queue(mock_redis):
    response = client.post("/jobs")
    assert response.status_code == 200
    assert mock_redis.lpush.called

def test_create_job_sets_status(mock_redis):
    response = client.post("/jobs")
    assert response.status_code == 200
    assert mock_redis.hset.called
