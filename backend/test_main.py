import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AutoDev API is running"}

def test_register():
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code in [200, 400]  # 400 if already exists

def test_login():
    # First register
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    
    # Then login
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
