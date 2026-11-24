from __future__ import annotations

# ruff: noqa: I001

from collections.abc import Generator

import pytest

from atlas_order_services import database
from atlas_order_services.config import get_settings
from atlas_order_services.main import app
from atlas_order_services.seed import load_sample_data
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient]:
    database_path = tmp_path / "atlas-test.db"
    monkeypatch.setenv("ATLAS_DATABASE_URL", f"sqlite+pysqlite:///{database_path.as_posix()}")
    monkeypatch.setenv("ATLAS_DOCUMENT_ROOT", str(tmp_path / "documents"))
    get_settings.cache_clear()
    database.configure_database(get_settings().database_url)
    database.Base.metadata.create_all(database.engine)
    load_sample_data()
    with TestClient(app) as test_client:
        yield test_client
    database.Base.metadata.drop_all(database.engine)
    get_settings.cache_clear()


@pytest.fixture()
def operator_headers() -> dict[str, str]:
    return {"Authorization": "Bearer atlas-demo-operator-token"}


@pytest.fixture()
def administrator_headers() -> dict[str, str]:
    return {"Authorization": "Bearer atlas-demo-admin-token"}
