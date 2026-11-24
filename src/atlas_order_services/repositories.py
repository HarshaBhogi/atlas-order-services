from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from .models import AuditEvent, Customer, DocumentRecord, Order, Product


class CustomerRepository:
    def get(self, session: Session, customer_id: int) -> Customer | None:
        return session.get(Customer, customer_id)

    def list(self, session: Session, offset: int, limit: int) -> tuple[list[Customer], int]:
        rows = session.scalars(select(Customer).order_by(Customer.id).offset(offset).limit(limit)).all()
        total = session.scalar(select(func.count()).select_from(Customer)) or 0
        return list(rows), total

    def add(self, session: Session, customer: Customer) -> Customer:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer


class ProductRepository:
    def get(self, session: Session, product_id: int) -> Product | None:
        return session.get(Product, product_id)

    def list(self, session: Session, offset: int, limit: int) -> tuple[list[Product], int]:
        query = select(Product).where(Product.active.is_(True)).order_by(Product.id)
        rows = session.scalars(query.offset(offset).limit(limit)).all()
        total = session.scalar(
            select(func.count()).select_from(Product).where(Product.active.is_(True))
        ) or 0
        return list(rows), total


class OrderRepository:
    def get(self, session: Session, order_id: int) -> Order | None:
        query = select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        return session.scalar(query)

    def list(self, session: Session, offset: int, limit: int) -> tuple[list[Order], int]:
        query = select(Order).order_by(Order.id).options(selectinload(Order.items))
        rows = session.scalars(query.offset(offset).limit(limit)).all()
        total = session.scalar(select(func.count()).select_from(Order)) or 0
        return list(rows), total


class DocumentRepository:
    def get_by_storage_name(self, session: Session, storage_name: str) -> DocumentRecord | None:
        return session.scalar(select(DocumentRecord).where(DocumentRecord.storage_name == storage_name))

    def add(self, session: Session, document: DocumentRecord) -> DocumentRecord:
        session.add(document)
        session.commit()
        session.refresh(document)
        return document


class AuditRepository:
    def record(self, session: Session, event: AuditEvent) -> AuditEvent:
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

    def list(self, session: Session, offset: int, limit: int) -> tuple[list[AuditEvent], int]:
        rows = session.scalars(select(AuditEvent).order_by(AuditEvent.id.desc()).offset(offset).limit(limit)).all()
        total = session.scalar(select(func.count()).select_from(AuditEvent)) or 0
        return list(rows), total
