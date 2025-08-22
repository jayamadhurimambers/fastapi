import pytest
from httpx import AsyncClient
import random

BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_create_patient():
    async with AsyncClient(base_url=BASE_URL) as ac:
        email = f"john{random.randint(1,10000)}@example.com"
        response = await ac.post(
            "/patients/",
            json={
                "name": "John Doe",
                "room_number": 101,
                "address": "123 Main St",
                "email": email
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["room_number"] == 101
        assert data["address"] == "123 Main St"
        assert data["email"] == email
        assert "id" in data


@pytest.mark.asyncio
async def test_list_patients_scroll():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.get("/patients/scroll/?after_id=0&limit=5")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_patient():
    async with AsyncClient(base_url=BASE_URL) as ac:
        email = f"jane{random.randint(1,10000)}@example.com"
        create_resp = await ac.post(
            "/patients/",
            json={
                "name": "Jane Doe",
                "room_number": 102,
                "address": "456 Main St",
                "email": email
            }
        )
        assert create_resp.status_code == 200
        patient_id = create_resp.json()["id"]
        get_resp = await ac.get(f"/patients/{patient_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == patient_id

@pytest.mark.asyncio
async def test_delete_patient():
    async with AsyncClient(base_url=BASE_URL) as ac:
        email = f"mark{random.randint(1,10000)}@example.com"
        create_resp = await ac.post(
            "/patients/",
            json={
                "name": "Mark Smith",
                "room_number": 103,
                "address": "789 Main St",
                "email": email
            }
        )
        assert create_resp.status_code == 200
        patient_id = create_resp.json()["id"]
        del_resp = await ac.delete(f"/patients/{patient_id}")
        assert del_resp.status_code == 200
        assert del_resp.json()["message"] == "Patient deleted successfully"
