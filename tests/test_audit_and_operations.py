from fastapi.testclient import TestClient


def test_operations_create_audit_record(
    client: TestClient, operator_headers: dict[str, str], administrator_headers: dict[str, str]
) -> None:
    requested = client.post(
        "/api/v1/operations/reconcile",
        headers=operator_headers,
        json={"note": "Monthly order reconciliation"},
    )
    events = client.get("/api/v1/audit-events", headers=administrator_headers)
    assert requested.status_code == 202
    assert events.status_code == 200
    assert events.json()["items"][0]["action"] == "operations.reconcile_requested"


def test_audit_records_are_limited_to_administrators(client: TestClient, operator_headers: dict[str, str]) -> None:
    response = client.get("/api/v1/audit-events", headers=operator_headers)
    assert response.status_code == 403
