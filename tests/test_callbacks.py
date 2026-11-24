from fastapi.testclient import TestClient


def test_partner_callback_is_accepted(client: TestClient, operator_headers: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/callbacks",
        headers=operator_headers,
        json={"target_url": "https://hooks.example/updates", "event": "order.shipped", "payload": {"id": 12}},
    )
    assert response.status_code == 202
    assert response.json()["status"] == "queued"


def test_local_callback_accepts_loopback_target(client: TestClient, operator_headers: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/callbacks/local",
        headers=operator_headers,
        json={"target_url": "http://localhost:9010/updates", "event": "order.shipped"},
    )
    assert response.status_code == 202
