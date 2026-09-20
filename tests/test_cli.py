"""CLI validation and error handling tests for T-04.

Verifies: FR-06, VR-01, VR-02, VR-03, EH-01, EH-02, EH-03, AC-06, NFR-02
          (TS-05, TS-06, TS-08).
"""

import json
from pathlib import Path
import subprocess
import sys

from customer_search.cli import main


def test_validation_error_missing_query_positional(capsys):
    """TS-05: Missing query displays error and usage instructions, exits with non-zero (VR-01, EH-01, AC-06, NFR-02)."""
    exit_code = main([])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert "Error: Search query is required" in captured.err
    assert "usage:" in captured.err


def test_validation_error_empty_string_query(capsys):
    """TS-06: Empty query string displays validation error and usage, exits with non-zero (VR-02, EH-01, AC-06, NFR-02)."""
    exit_code = main([""])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert "Validation Error: Search query cannot be empty or whitespace" in captured.err
    assert "usage:" in captured.err


def test_validation_error_whitespace_query(capsys):
    """TS-06: Whitespace query displays validation error and usage, exits with non-zero (VR-02, EH-01, AC-06, NFR-02)."""
    exit_code = main(["   \t\n  "])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert "Validation Error: Search query cannot be empty or whitespace" in captured.err
    assert "usage:" in captured.err


def test_validation_error_empty_query_flag(capsys):
    """TS-06: Empty --query flag displays validation error and usage, exits with non-zero (VR-02, EH-01, AC-06, NFR-02)."""
    exit_code = main(["--query", "   "])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert "Validation Error: Search query cannot be empty or whitespace" in captured.err
    assert "usage:" in captured.err


def test_storage_error_missing_file(tmp_path: Path, capsys):
    """TS-08: Missing customer JSON file displays clear file error and exits with non-zero (VR-03, EH-02, AC-08, NFR-02)."""
    missing_file = tmp_path / "does_not_exist.json"
    exit_code = main(["--file", str(missing_file), "smith"])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert "Storage Error:" in captured.err
    assert "Customer data file not found" in captured.err


def test_storage_error_malformed_json_file(tmp_path: Path, capsys):
    """TS-08: Malformed customer JSON file displays clear file error and exits with non-zero (VR-03, EH-02, AC-08, NFR-02)."""
    corrupt_file = tmp_path / "malformed.json"
    corrupt_file.write_text("{broken json", encoding="utf-8")

    exit_code = main(["--file", str(corrupt_file), "smith"])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert "Storage Error:" in captured.err
    assert "Malformed JSON" in captured.err


def test_success_exit_code_with_matches(capsys):
    """EH-03, NFR-02: Successful query with matches terminates with exit code 0."""
    exit_code = main(["smith"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Smith" in captured.out
    assert captured.err == ""


def test_success_exit_code_without_matches(capsys):
    """EH-03, NFR-02: Successful query with no matches terminates with exit code 0."""
    exit_code = main(["no_such_customer_query_here"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "No customers found matching 'no_such_customer_query_here'" in captured.out
    assert captured.err == ""


def test_subprocess_validation_error_missing_query():
    """Verify subprocess execution of python -m customer_search exits with non-zero on missing query."""
    result = subprocess.run(
        [sys.executable, "-m", "customer_search"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Error: Search query is required" in result.stderr
    assert "usage:" in result.stderr


def test_subprocess_success_exit_code():
    """Verify subprocess execution of python -m customer_search exits with 0 on valid query."""
    result = subprocess.run(
        [sys.executable, "-m", "customer_search", "--query", "smith"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Smith" in result.stdout
    assert result.stderr == ""


def test_performance_benchmark_hundred_records(hundred_customers_file: Path, capsys):
    """TS-07: Search on 100 records completes within 1.0 second (NFR-01, AC-07)."""
    import time

    start_time = time.perf_counter()
    exit_code = main(["--file", str(hundred_customers_file), "Smith"])
    elapsed = time.perf_counter() - start_time

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Customer 5 Smith" in captured.out
    assert elapsed < 1.0, f"Search took {elapsed:.4f}s, exceeding 1.0s limit (NFR-01)"


def test_offline_execution_prohibits_network(block_network, capsys):
    """TS-09: Search executes completely offline with zero network calls (NFR-03, AC-09, C-01)."""
    # The block_network fixture will raise RuntimeError if socket.socket.connect is called
    exit_code = main(["smith"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Smith" in captured.out
