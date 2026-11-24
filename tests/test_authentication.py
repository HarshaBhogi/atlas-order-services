from fastapi.testclient import TestClient


def test_customer_list_requires_bearer_token(client: TestClient) -> None:
    response = client.get("/api/v1/customers")
    assert response.status_code == 401


def test_token_can_be_requested_for_local_operator(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/token",
        json={"username": "operator", "password": "atlas-demo-password"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
