from __future__ import annotations

from pathlib import Path


class DocumentStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def read_by_name(self, document_name: str) -> str:
        location = self.root / document_name
        return location.read_text(encoding="utf-8")

    def write_by_name(self, document_name: str, content: str) -> Path:
        root = self.root.resolve()
        location = (root / document_name).resolve()
        try:
            location.relative_to(root)
        except ValueError as exc:
            raise ValueError("Document name is outside the configured store") from exc
        location.parent.mkdir(parents=True, exist_ok=True)
        location.write_text(content, encoding="utf-8")
        return location
