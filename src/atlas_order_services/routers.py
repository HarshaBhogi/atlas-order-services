from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from .auth import Principal, current_principal, issue_token, require_role
from .config import Settings, get_settings
from .database import get_session
from .partner_client import PartnerClient
from .product_queries import catalog_search, filtered_products
from .repositories import AuditRepository, CustomerRepository, OrderRepository, ProductRepository
from .schemas import (
    AuditEventRead,
    CallbackReceipt,
    CallbackRequest,
    CustomerCreate,
    CustomerRead,
    DocumentRead,
    DocumentWrite,
    OrderCreate,
    OrderRead,
    Page,
    ProductRead,
    ReconcileRequest,
    TokenRequest,
    TokenResponse,
)
from .services import AuditService, CustomerService, DocumentService, OrderService

router = APIRouter(prefix="/api/v1")
SessionDependency = Annotated[Session, Depends(get_session)]
PrincipalDependency = Annotated[Principal, Depends(current_principal)]


def page_values(offset: int, limit: int, settings: Settings) -> tuple[int, int]:
    checked_offset = max(offset, 0)
    checked_limit = min(max(limit, 1), settings.page_size_max)
    return checked_offset, checked_limit


def correlation_id(request: Request) -> str:
    return request.headers.get("x-correlation-id", "not-provided")


@router.post("/auth/token", response_model=TokenResponse)
def create_token(payload: TokenRequest) -> TokenResponse:
    token = issue_token(payload.username, payload.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credentials not accepted")
    return TokenResponse(access_token=token)


@router.get("/customers", response_model=Page[CustomerRead])
def list_customers(
    session: SessionDependency,
    _: PrincipalDependency,
    offset: int = Query(default=0),
    limit: int = Query(default=20),
    settings: Settings = Depends(get_settings),
) -> Page[CustomerRead]:
    offset, limit = page_values(offset, limit, settings)
    records, total = CustomerRepository().list(session, offset, limit)
    return Page[CustomerRead](items=records, offset=offset, limit=limit, total=total)


@router.post("/customers", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(session: SessionDependency, _: PrincipalDependency, payload: CustomerCreate) -> CustomerRead:
    return CustomerRead.model_validate(CustomerService().create(session, payload))


@router.get("/customers/{customer_id}", response_model=CustomerRead)
def get_customer(session: SessionDependency, _: PrincipalDependency, customer_id: int) -> CustomerRead:
    return CustomerRead.model_validate(CustomerService().get_or_404(session, customer_id))


@router.get("/products", response_model=Page[ProductRead])
def list_products(
    session: SessionDependency,
    _: PrincipalDependency,
    offset: int = Query(default=0),
    limit: int = Query(default=20),
    settings: Settings = Depends(get_settings),
) -> Page[ProductRead]:
    offset, limit = page_values(offset, limit, settings)
    records, total = ProductRepository().list(session, offset, limit)
    return Page[ProductRead](items=records, offset=offset, limit=limit, total=total)


@router.get("/products/search", response_model=list[ProductRead])
def search_products(session: SessionDependency, _: PrincipalDependency, q: str = Query(min_length=1)) -> list[ProductRead]:
    return [ProductRead.model_validate(product) for product in catalog_search(session, q)]


@router.get("/products/browse", response_model=list[ProductRead])
def browse_products(
    session: SessionDependency,
    _: PrincipalDependency,
    q: str = Query(default="", max_length=80),
    sort: str = Query(default="name"),
) -> list[ProductRead]:
    return [ProductRead.model_validate(product) for product in filtered_products(session, q, sort)]


@router.get("/orders", response_model=Page[OrderRead])
def list_orders(
    session: SessionDependency,
    _: PrincipalDependency,
    offset: int = Query(default=0),
    limit: int = Query(default=20),
    settings: Settings = Depends(get_settings),
) -> Page[OrderRead]:
    offset, limit = page_values(offset, limit, settings)
    records, total = OrderRepository().list(session, offset, limit)
    return Page[OrderRead](items=records, offset=offset, limit=limit, total=total)


@router.post("/orders", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    request: Request, session: SessionDependency, principal: PrincipalDependency, payload: OrderCreate
) -> OrderRead:
    return OrderRead.model_validate(
        OrderService().create(session, payload, principal.subject, correlation_id(request))
    )


@router.get("/orders/{order_id}", response_model=OrderRead)
def get_order(session: SessionDependency, _: PrincipalDependency, order_id: int) -> OrderRead:
    order = OrderRepository().get(session, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return OrderRead.model_validate(order)


@router.get("/documents/{name:path}", response_model=DocumentRead)
def get_document(session: SessionDependency, _: PrincipalDependency, name: str) -> DocumentRead:
    service = DocumentService(get_settings().document_root)
    return DocumentRead(name=name, content=service.read(session, name))


@router.put("/documents/{name:path}", status_code=status.HTTP_201_CREATED)
def put_document(
    session: SessionDependency, _: PrincipalDependency, name: str, payload: DocumentWrite
) -> dict[str, str]:
    service = DocumentService(get_settings().document_root)
    record = service.write(session, name, payload)
    return {"name": record.storage_name, "status": "stored"}


@router.post("/callbacks", response_model=CallbackReceipt, status_code=status.HTTP_202_ACCEPTED)
def send_callback(_: PrincipalDependency, payload: CallbackRequest) -> CallbackReceipt:
    return CallbackReceipt(**PartnerClient().send_event(str(payload.target_url), payload.event, payload.payload))


@router.post("/callbacks/local", response_model=CallbackReceipt, status_code=status.HTTP_202_ACCEPTED)
def send_local_callback(_: PrincipalDependency, payload: CallbackRequest) -> CallbackReceipt:
    try:
        response = PartnerClient().send_local_event(str(payload.target_url), payload.event, payload.payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return CallbackReceipt(**response)


@router.get("/audit-events", response_model=Page[AuditEventRead])
def list_audit_events(
    session: SessionDependency,
    _: Annotated[Principal, Depends(require_role("administrator"))],
    offset: int = Query(default=0),
    limit: int = Query(default=20),
    settings: Settings = Depends(get_settings),
) -> Page[AuditEventRead]:
    offset, limit = page_values(offset, limit, settings)
    records, total = AuditRepository().list(session, offset, limit)
    return Page[AuditEventRead](items=records, offset=offset, limit=limit, total=total)


@router.post("/operations/reconcile", status_code=status.HTTP_202_ACCEPTED)
def reconcile_orders(
    request: Request, session: SessionDependency, principal: PrincipalDependency, payload: ReconcileRequest
) -> dict[str, str]:
    AuditService().record(
        session,
        actor=principal.subject,
        action="operations.reconcile_requested",
        correlation_id=correlation_id(request),
        details={"note": payload.note},
    )
    return {"status": "accepted"}


def add_probe_routes(app_router: APIRouter) -> None:
    @app_router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app_router.get("/ready")
    def ready(session: SessionDependency) -> dict[str, str]:
        session.connection()
        return {"status": "ready"}


probes = APIRouter()
add_probe_routes(probes)
