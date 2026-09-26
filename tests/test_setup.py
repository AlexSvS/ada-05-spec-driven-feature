"""Test project environment and setup for T-01 (C-01, C-02, NFR-03, AC-09)."""

import json
from pathlib import Path
import sys


def test_python_version():
    """Verify runtime environment meets C-02 (Python 3.11+)."""
    assert sys.version_info >= (3, 11), f"Requires Python 3.11+, found {sys.version}"


def test_package_import():
    """Verify customer_search package is importable and has version."""
    import customer_search

    assert hasattr(customer_search, "__version__")
    assert customer_search.__version__ == "0.2.0"


def test_customers_json_exists_and_valid():
    """Verify default customers.json exists and contains valid customer records."""
    customers_file = Path("customers.json")
    assert customers_file.is_file(), "customers.json must exist in project root"

    with open(customers_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list), "customers.json must contain a list of records"
    assert len(data) > 0, "customers.json should contain initial records"
    for record in data:
        assert "id" in record and isinstance(record["id"], int)
        assert "name" in record and isinstance(record["name"], str)
        assert "email" in record and isinstance(record["email"], str)


def test_no_external_dependencies():
    """Verify project dependencies in pyproject.toml are empty (NFR-03, C-01)."""
    pyproject_file = Path("pyproject.toml")
    assert pyproject_file.is_file(), "pyproject.toml must exist"

    content = pyproject_file.read_text(encoding="utf-8")
    assert "dependencies = []" in content, "Dependencies should be empty to ensure offline stdlib-only execution"
