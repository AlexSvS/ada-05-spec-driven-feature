"""Unit and service tests for CustomerService search logic.

Verifies: FR-01, FR-02, FR-03, FR-04, FR-05, SR-01, SR-02, SR-03, SR-04, SR-05,
          AC-01, AC-02, AC-03, AC-04, AC-05 (TS-01, TS-02, TS-03, TS-04).
"""

from customer_search.cli import format_customer, main
from customer_search.models import Customer
from customer_search.service import CustomerService, ValidationError


class FakeStorage:
    """Mock storage providing fixed customer records for testing."""

    def __init__(self, records: list[dict] | None = None) -> None:
        self.records = records if records is not None else [
            {"id": 1, "name": "John Smith", "email": "john.smith@example.com"},
            {"id": 2, "name": "Jane Doe", "email": "jane.doe@example.com"},
            {"id": 3, "name": "Bob Johnson", "email": "bob.johnson@corp.net"},
            {"id": 4, "name": "Alice Smith", "email": "alice.smith@domain.org"},
        ]

    def read_all(self) -> list[dict]:
        return self.records


def test_search_partial_name_match():
    """TS-01: Partial substring search matches customer name (SR-01, AC-02)."""
    service = CustomerService(storage=FakeStorage())
    results = service.search("john")

    assert len(results) == 2
    names = [c.name for c in results]
    assert "John Smith" in names
    assert "Bob Johnson" in names


def test_search_name_case_insensitivity():
    """TS-01: Case-insensitivity in name search (SR-01, AC-02)."""
    service = CustomerService(storage=FakeStorage())
    results_lower = service.search("jane")
    results_upper = service.search("JANE")
    results_mixed = service.search("JaNe")

    assert results_lower == results_upper == results_mixed
    assert len(results_lower) == 1
    assert results_lower[0].name == "Jane Doe"


def test_search_partial_email_match():
    """TS-02: Partial substring search matches customer email (SR-02, AC-03)."""
    service = CustomerService(storage=FakeStorage())
    results = service.search("corp.net")

    assert len(results) == 1
    assert results[0].name == "Bob Johnson"
    assert results[0].email == "bob.johnson@corp.net"


def test_search_email_case_insensitivity():
    """TS-02: Case-insensitivity in email search (SR-02, AC-03)."""
    service = CustomerService(storage=FakeStorage())
    results_lower = service.search("example.com")
    results_upper = service.search("EXAMPLE.COM")

    assert results_lower == results_upper
    assert len(results_lower) == 2


def test_search_or_condition():
    """SR-03: Matches if either name OR email matches the query."""
    custom_records = [
        {"id": 1, "name": "Alice Wonderland", "email": "rabbit@hole.com"},
        {"id": 2, "name": "Mad Hatter", "email": "alice.fan@tea.com"},
    ]
    service = CustomerService(storage=FakeStorage(custom_records))
    results = service.search("alice")

    assert len(results) == 2
    assert results[0].id == 1  # matched on name
    assert results[1].id == 2  # matched on email


def test_search_no_match_returns_empty_list():
    """TS-04: Searching with non-matching query returns empty list (SR-05, AC-05)."""
    service = CustomerService(storage=FakeStorage())
    results = service.search("nonexistentquery")

    assert results == []


def test_search_preserves_encounter_order():
    """OQ-02: Results preserve the order of appearance in storage."""
    service = CustomerService(storage=FakeStorage())
    results = service.search("smith")

    assert len(results) == 2
    assert results[0].id == 1
    assert results[1].id == 4


def test_format_customer_output():
    """TS-03: Matching customer records display ID, name, and email (SR-04, AC-04)."""
    customer = Customer(id=42, name="Test User", email="test@user.com")
    formatted = format_customer(customer)

    assert "ID: 42" in formatted
    assert "Name: Test User" in formatted
    assert "Email: test@user.com" in formatted


def test_cli_presentation_with_flag(capsys):
    """AC-01, AC-04: CLI with --query displays matching customers."""
    service = CustomerService(storage=FakeStorage())
    exit_code = main(["--query", "jane"], service=service)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Jane Doe" in captured.out
    assert "jane.doe@example.com" in captured.out


def test_cli_presentation_with_positional(capsys):
    """AC-01, AC-04: CLI with positional argument displays matching customers."""
    service = CustomerService(storage=FakeStorage())
    exit_code = main(["smith"], service=service)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "John Smith" in captured.out
    assert "Alice Smith" in captured.out


def test_cli_no_match_notification(capsys):
    """TS-04: CLI displays notification message and exits with 0 on no matches (SR-05, AC-05)."""
    service = CustomerService(storage=FakeStorage())
    exit_code = main(["xyz123"], service=service)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "No customers found matching 'xyz123'" in captured.out


def test_service_validation_empty_query():
    """VR-02: Service search raises ValidationError on empty string."""
    import pytest

    service = CustomerService(storage=FakeStorage())
    with pytest.raises(ValidationError, match="Search query cannot be empty or whitespace"):
        service.search("")


def test_service_validation_whitespace_query():
    """VR-02: Service search raises ValidationError on whitespace-only string."""
    import pytest

    service = CustomerService(storage=FakeStorage())
    with pytest.raises(ValidationError, match="Search query cannot be empty or whitespace"):
        service.search("   \t  ")

