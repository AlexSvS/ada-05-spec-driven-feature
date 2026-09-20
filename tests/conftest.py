"""Shared pytest fixtures for customer search test suite."""

import json
from pathlib import Path
import socket
from typing import Any, Generator
import pytest


@pytest.fixture
def sample_customers_data() -> list[dict[str, Any]]:
    """Fixture providing a standard list of customer record dictionaries."""
    return [
        {"id": 1, "name": "John Smith", "email": "john.smith@example.com"},
        {"id": 2, "name": "Jane Doe", "email": "jane.doe@example.com"},
        {"id": 3, "name": "Bob Johnson", "email": "bob.johnson@corp.net"},
        {"id": 4, "name": "Alice Smith", "email": "alice.smith@domain.org"},
    ]


@pytest.fixture
def hundred_customers_data() -> list[dict[str, Any]]:
    """Fixture providing exactly 100 valid customer records for performance tests (NFR-01)."""
    return [
        {
            "id": i,
            "name": f"Customer {i} {'Smith' if i % 5 == 0 else 'Doe'}",
            "email": f"customer{i}@{'example.com' if i % 2 == 0 else 'domain.org'}",
        }
        for i in range(1, 101)
    ]


@pytest.fixture
def hundred_customers_file(
    tmp_path: Path, hundred_customers_data: list[dict[str, Any]]
) -> Path:
    """Fixture providing a temporary customers.json file containing 100 customer records."""
    file_path = tmp_path / "customers_100.json"
    file_path.write_text(json.dumps(hundred_customers_data, indent=2), encoding="utf-8")
    return file_path


@pytest.fixture
def block_network(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Fixture to ensure offline execution (NFR-03, AC-09) by preventing socket connections."""
    def guarded_connect(*args, **kwargs):
        raise RuntimeError("Network connection prohibited: execution must be offline (NFR-03, C-01).")

    monkeypatch.setattr(socket.socket, "connect", guarded_connect)
    yield
