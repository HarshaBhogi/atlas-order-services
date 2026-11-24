from fastapi.testclient import TestClient


def test_order_creation_calculates_total(client: TestClient, operator_headers: dict[str, str]) -> None:
    response = client.post(
        "/api/v1/orders",
        headers={**operator_headers, "x-correlation-id": "order-check-001"},
        json={"customer_id": 1, "items": [{"product_id": 1, "quantity": 2}]},
    )
    assert response.status_code == 201
    assert response.json()["total_cents"] == 37800


def test_order_list_and_fetch(client: TestClient, operator_headers: dict[str, str]) -> None:
    listing = client.get("/api/v1/orders", headers=operator_headers)
    order_id = listing.json()["items"][0]["id"]
    fetched = client.get(f"/api/v1/orders/{order_id}", headers=operator_headers)
    assert listing.status_code == 200
    assert fetched.status_code == 200
    assert fetched.json()["items"]
