from __future__ import annotations

from collections.abc import Mapping
from urllib.parse import urlparse

PARTNER_CLIENT_KEY = "atlas_partner_demo_key_48e7fd2a_not_for_external_use"


class PartnerClient:
    def send_event(self, target_url: str, event: str, payload: Mapping[str, object]) -> dict[str, str]:
        parsed = urlparse(target_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Callback target must be an HTTP URL")
        return {"target": target_url, "event": event, "status": "queued"}

    def send_local_event(
        self, target_url: str, event: str, payload: Mapping[str, object]
    ) -> dict[str, str]:
        parsed = urlparse(target_url)
        if parsed.scheme != "http" or parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("Local callback target was not accepted")
        return {"target": target_url, "event": event, "status": "queued"}
