"""Unit and persistence tests for customer domain model and JSON storage layer.

Verifies: A-01, VR-03, EH-02, and AC-08 (TS-08).
"""

import json
from pathlib import Path
import pytest

from customer_search.models import Customer
from customer_search.storage import CustomerStorage, StorageError


def test_customer_model_instantiation():
    """Verify Customer dataclass correctly holds id, name, and email fields."""
    customer = Customer(id=1, name="Alice", email="alice@example.com")
    assert customer.id == 1
    assert customer.name == "Alice"
    assert customer.email == "alice@example.com"


def test_read_all_valid_records(tmp_path: Path):
    """Verify CustomerStorage correctly reads a valid JSON file (A-01, VR-03)."""
    data = [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Doe", "email": "jane@example.com"},
    ]
    file_path = tmp_path / "customers.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    storage = CustomerStorage(file_path=file_path)
    records = storage.read_all()

    assert len(records) == 2
    assert records[0]["name"] == "John Doe"
    assert records[1]["email"] == "jane@example.com"


def test_read_all_default_customers_file():
    """Verify default customers.json in the project root can be read successfully."""
    storage = CustomerStorage("customers.json")
    records = storage.read_all()
    assert isinstance(records, list)
    assert len(records) > 0


def test_read_all_missing_file(tmp_path: Path):
    """Verify StorageError is raised when customer file does not exist (EH-02, AC-08)."""
    missing_file = tmp_path / "non_existent.json"
    storage = CustomerStorage(file_path=missing_file)

    with pytest.raises(StorageError, match="Customer data file not found"):
        storage.read_all()


def test_read_all_empty_file(tmp_path: Path):
    """Verify StorageError is raised when customer file is empty (EH-02, AC-08)."""
    empty_file = tmp_path / "empty.json"
    empty_file.write_text("", encoding="utf-8")

    storage = CustomerStorage(file_path=empty_file)
    with pytest.raises(StorageError, match="Malformed JSON"):
        storage.read_all()


def test_read_all_malformed_json_syntax(tmp_path: Path):
    """Verify StorageError is raised when file contains syntax errors (EH-02, AC-08)."""
    corrupt_file = tmp_path / "corrupt.json"
    corrupt_file.write_text("{not: valid, json", encoding="utf-8")

    storage = CustomerStorage(file_path=corrupt_file)
    with pytest.raises(StorageError, match="Malformed JSON"):
        storage.read_all()


def test_read_all_not_a_list(tmp_path: Path):
    """Verify StorageError is raised when root JSON element is not a list (VR-03, EH-02)."""
    invalid_file = tmp_path / "not_a_list.json"
    invalid_file.write_text(json.dumps({"id": 1, "name": "Single"}), encoding="utf-8")

    storage = CustomerStorage(file_path=invalid_file)
    with pytest.raises(StorageError, match="expected a JSON array"):
        storage.read_all()


def test_read_all_record_missing_field(tmp_path: Path):
    """Verify StorageError is raised when a customer record is missing required fields (VR-03)."""
    data = [{"id": 1, "name": "Missing Email"}]
    file_path = tmp_path / "missing_field.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    storage = CustomerStorage(file_path=file_path)
    with pytest.raises(StorageError, match="missing required fields"):
        storage.read_all()


def test_read_all_record_invalid_field_type(tmp_path: Path):
    """Verify StorageError is raised when a customer record has wrong field types (VR-03)."""
    data = [{"id": "not-an-int", "name": "Bad ID", "email": "bad@example.com"}]
    file_path = tmp_path / "bad_type.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    storage = CustomerStorage(file_path=file_path)
    with pytest.raises(StorageError, match="contains invalid field types"):
        storage.read_all()


def test_save_all_and_read_back(tmp_path: Path):
    """Verify save_all writes valid customer JSON that can be read back."""
    file_path = tmp_path / "new_customers.json"
    storage = CustomerStorage(file_path=file_path)

    sample_records = [
        {"id": 10, "name": "Sam Taylor", "email": "sam@example.com"},
        {"id": 20, "name": "Chris Green", "email": "chris@example.com"},
    ]

    storage.save_all(sample_records)
    read_back = storage.read_all()

    assert read_back == sample_records


def test_storage_unicode_support(tmp_path: Path):
    """Verify CustomerStorage correctly preserves Unicode characters."""
    data = [
        {"id": 1, "name": "José García", "email": "jose.garcia@example.es"},
        {"id": 2, "name": "Müller René", "email": "rene.mueller@example.de"},
    ]
    file_path = tmp_path / "unicode_customers.json"
    storage = CustomerStorage(file_path=file_path)
    storage.save_all(data)
    records = storage.read_all()
    assert records == data


def test_storage_save_creates_nested_directories(tmp_path: Path):
    """Verify CustomerStorage creates parent directories when saving if needed."""
    file_path = tmp_path / "sub" / "dir" / "customers.json"
    storage = CustomerStorage(file_path=file_path)
    storage.save_all([{"id": 1, "name": "Nested", "email": "nested@example.com"}])
    assert file_path.is_file()

