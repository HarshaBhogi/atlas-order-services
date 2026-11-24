from fastapi.testclient import TestClient


def test_customer_create_and_fetch(client: TestClient, operator_headers: dict[str, str]) -> None:
    created = client.post(
        "/api/v1/customers",
        headers=operator_headers,
        json={"external_ref": "CUS-2001", "name": "Juniper Outlet", "email": "hello@juniper.example"},
    )
    assert created.status_code == 201
    customer_id = created.json()["id"]

    fetched = client.get(f"/api/v1/customers/{customer_id}", headers=operator_headers)
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Juniper Outlet"


def test_customer_payload_is_checked(client: TestClient, operator_headers: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/customers",
        headers=operator_headers,
        json={"external_ref": "x", "name": "", "email": "not-an-email"},
    )
    assert response.status_code == 422
