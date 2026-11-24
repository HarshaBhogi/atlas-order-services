from fastapi.testclient import TestClient


def test_document_can_be_recorded_and_read(client: TestClient, operator_headers: dict[str, str]) -> None:
    stored = client.put(
        "/api/v1/documents/customer-note.txt",
        headers=operator_headers,
        json={"customer_id": 1, "content": "Delivery window: Thursday", "content_type": "text/plain"},
    )
    fetched = client.get("/api/v1/documents/customer-note.txt", headers=operator_headers)
    assert stored.status_code == 201
    assert fetched.json()["content"] == "Delivery window: Thursday"


def test_document_requires_known_customer(client: TestClient, operator_headers: dict[str, str]) -> None:
    response = client.put(
        "/api/v1/documents/missing-customer.txt",
        headers=operator_headers,
        json={"customer_id": 9999, "content": "Note"},
    )
    assert response.status_code == 404
