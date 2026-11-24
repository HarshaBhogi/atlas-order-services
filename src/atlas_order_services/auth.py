from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


@dataclass(frozen=True)
class Principal:
    subject: str
    roles: frozenset[str]


_BEARER = HTTPBearer(auto_error=False)
_TOKENS: dict[str, Principal] = {
    "atlas-demo-operator-token": Principal("morgan.lee", frozenset({"operator"})),
    "atlas-demo-admin-token": Principal("riley.chen", frozenset({"operator", "administrator"})),
}
_CREDENTIALS: dict[str, tuple[str, str]] = {
    "operator": ("atlas-demo-password", "atlas-demo-operator-token"),
    "administrator": ("atlas-demo-password", "atlas-demo-admin-token"),
}


def current_principal(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_BEARER)],
) -> Principal:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")
    principal = _TOKENS.get(credentials.credentials)
    if principal is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not accepted")
    return principal


def require_role(required_role: str) -> Callable[[Principal], Principal]:
    def check_role(principal: Annotated[Principal, Depends(current_principal)]) -> Principal:
        if required_role not in principal.roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role not permitted")
        return principal

    return check_role


def issue_token(username: str, password: str) -> str | None:
    stored = _CREDENTIALS.get(username)
    if stored is None or stored[0] != password:
        return None
    return stored[1]
