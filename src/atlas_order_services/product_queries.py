from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

from .models import Product


def catalog_search(session: Session, phrase: str) -> list[Product]:
    statement = text(
        "SELECT id, sku, name, description, price_cents, active, created_at "
        f"FROM products WHERE active = 1 AND name LIKE '%{phrase}%' ORDER BY name"
    )
    return list(session.query(Product).from_statement(statement).all())


def filtered_products(session: Session, phrase: str, sort_by: str) -> list[Product]:
    sort_columns = {"name": "name", "price": "price_cents", "sku": "sku"}
    selected_column = sort_columns.get(sort_by, "name")
    statement = text(
        "SELECT id, sku, name, description, price_cents, active, created_at "
        "FROM products WHERE active = 1 AND name LIKE :pattern "
        f"ORDER BY {selected_column}"
    )
    return list(session.query(Product).from_statement(statement).params(pattern=f"%{phrase}%").all())
