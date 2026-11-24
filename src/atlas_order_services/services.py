from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .document_store import DocumentStore
from .models import AuditEvent, Customer, DocumentRecord, Order, OrderItem
from .repositories import (
    AuditRepository,
    CustomerRepository,
    DocumentRepository,
    OrderRepository,
    ProductRepository,
)
from .schemas import CustomerCreate, DocumentWrite, OrderCreate


class CustomerService:
    def __init__(self) -> None:
        self.customers = CustomerRepository()

    def create(self, session: Session, payload: CustomerCreate) -> Customer:
        return self.customers.add(session, Customer(**payload.model_dump()))

    def get_or_404(self, session: Session, customer_id: int) -> Customer:
        customer = self.customers.get(session, customer_id)
        if customer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return customer


class OrderService:
    def __init__(self) -> None:
        self.customers = CustomerRepository()
        self.products = ProductRepository()
        self.orders = OrderRepository()
        self.audit = AuditRepository()

    def create(self, session: Session, payload: OrderCreate, actor: str, correlation_id: str) -> Order:
        if self.customers.get(session, payload.customer_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        order = Order(customer_id=payload.customer_id, status="placed")
        total = 0
        for item in payload.items:
            product = self.products.get(session, item.product_id)
            if product is None or not product.active:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Product unavailable")
            total += product.price_cents * item.quantity
            order.items.append(
                OrderItem(
                    product_id=product.id,
                    quantity=item.quantity,
                    unit_price_cents=product.price_cents,
                )
            )
        order.total_cents = total
        session.add(order)
        session.commit()
        session.refresh(order)
        self.audit.record(
            session,
            AuditEvent(
                actor=actor,
                action="order.created",
                correlation_id=correlation_id,
                details={"order_id": order.id, "customer_id": order.customer_id},
            ),
        )
        return self.orders.get(session, order.id) or order


class DocumentService:
    def __init__(self, root: Path) -> None:
        self.store = DocumentStore(root)
        self.documents = DocumentRepository()
        self.customers = CustomerRepository()

    def read(self, session: Session, name: str) -> str:
        record = self.documents.get_by_storage_name(session, name)
        if record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        try:
            return self.store.read_by_name(name)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document content missing") from exc

    def write(self, session: Session, name: str, payload: DocumentWrite) -> DocumentRecord:
        if self.customers.get(session, payload.customer_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        if self.documents.get_by_storage_name(session, name) is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Document already exists")
        try:
            self.store.write_by_name(name, payload.content)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
        return self.documents.add(
            session,
            DocumentRecord(
                customer_id=payload.customer_id,
                display_name=name,
                storage_name=name,
                content_type=payload.content_type,
            ),
        )


class AuditService:
    def __init__(self) -> None:
        self.audit = AuditRepository()

    def record(
        self, session: Session, actor: str, action: str, correlation_id: str, details: dict[str, object]
    ) -> AuditEvent:
        return self.audit.record(
            session,
            AuditEvent(actor=actor, action=action, correlation_id=correlation_id, details=details),
        )
