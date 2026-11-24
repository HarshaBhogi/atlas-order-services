from __future__ import annotations

from . import database
from .config import get_settings
from .document_store import DocumentStore
from .models import Customer, DocumentRecord, Order, OrderItem, Product


def _write_welcome_note() -> None:
    DocumentStore(get_settings().document_root).write_by_name(
        "welcome-note.txt", "Welcome to Atlas Order Services."
    )


def load_sample_data() -> None:
    with database.SessionLocal() as session:
        if session.query(Customer).count() > 0:
            _write_welcome_note()
            return
        customers = [
            Customer(external_ref="CUS-1001", name="Nova Mart", email="orders@nova-mart.example"),
            Customer(external_ref="CUS-1002", name="Saffron Supply", email="team@saffron-supply.example"),
            Customer(external_ref="CUS-1003", name="Harbor & Pine", email="billing@harbor-pine.example"),
        ]
        products = [
            Product(sku="AT-CHAIR-01", name="Atlas Task Chair", description="Adjustable mesh chair", price_cents=18900),
            Product(sku="AT-DESK-02", name="Atlas Standing Desk", description="Electric sit-stand desk", price_cents=59900),
            Product(sku="AT-LAMP-03", name="Atlas Desk Lamp", description="Dimmable LED lamp", price_cents=4900),
        ]
        session.add_all([*customers, *products])
        session.flush()
        order = Order(customer_id=customers[0].id, status="fulfilled", total_cents=23800)
        order.items = [
            OrderItem(product_id=products[0].id, quantity=1, unit_price_cents=18900),
            OrderItem(product_id=products[2].id, quantity=1, unit_price_cents=4900),
        ]
        document = DocumentRecord(
            customer_id=customers[0].id,
            display_name="welcome-note.txt",
            storage_name="welcome-note.txt",
            content_type="text/plain",
        )
        session.add_all([order, document])
        session.commit()
    _write_welcome_note()


if __name__ == "__main__":
    load_sample_data()
