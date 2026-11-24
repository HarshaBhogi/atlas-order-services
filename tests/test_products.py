from fastapi.testclient import TestClient


def test_product_list_supports_paging(client: TestClient, operator_headers: dict[str, str]) -> None:
    response = client.get("/api/v1/products?offset=0&limit=2", headers=operator_headers)
    body = response.json()
    assert response.status_code == 200
    assert len(body["items"]) == 2
    assert body["total"] == 3


def test_product_search_and_browse_return_records(
    client: TestClient, operator_headers: dict[str, str]
) -> None:
    search = client.get("/api/v1/products/search?q=Chair", headers=operator_headers)
    browse = client.get("/api/v1/products/browse?q=Atlas&sort=price", headers=operator_headers)
    assert [item["sku"] for item in search.json()] == ["AT-CHAIR-01"]
    assert len(browse.json()) == 3
