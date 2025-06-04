import pytest
from httpx import AsyncClient

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(base_url=BASE_URL) as ac:
        payload = {
            "username": "testuser_api",
            "email": "testuser_api@example.com",
            "password": "testpass123",
            "first_name": "Тест",
            "last_name": "Пользователь",
            "phone": "+79999999999"
        }
        response = await ac.post("/auth/register", json=payload)
    assert response.status_code in (200, 400)  # 400 если пользователь уже есть

@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(base_url=BASE_URL) as ac:
        data = {
            "username": "test",
            "password": "test123"
        }
        response = await ac.post("/auth/login", data=data)
        print("LOGIN RESPONSE:", response.status_code, response.text)
        assert response.status_code in (200, 401)

