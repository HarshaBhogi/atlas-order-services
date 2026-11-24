
from atlas_order_services import database
from atlas_order_services.repositories import CustomerRepository, ProductRepository


def test_repositories_return_seeded_pages(client) -> None:
    with database.SessionLocal() as session:
        customers, customer_total = CustomerRepository().list(session, 0, 2)
        products, product_total = ProductRepository().list(session, 0, 2)
    assert len(customers) == 2
    assert customer_total == 3
    assert len(products) == 2
    assert product_total == 3
