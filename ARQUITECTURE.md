# Architecture

## Overview
The Customer Search application is a modular, offline command-line tool developed in Python 3.11+. It enables users to search customer records by name or email from a local JSON dataset (`customers.json`). The system follows a layered architecture with clear separation of concerns among presentation, business logic, and data persistence.

## Components
The system is divided into three primary components:
- **CLI (Presentation Layer)**: Interprets command-line arguments, delegates search requests to the Customer Service, and formats results or error messages for the user.
- **Customer Service (Business Logic Layer)**: Applies validation rules, executes case-insensitive search logic across customer names and emails, and coordinates data access.
- **JSON Storage (Data Persistence Layer)**: Reads and writes customer data from/to `customers.json`, handling file I/O and JSON serialization/deserialization.

## Responsibilities
- **CLI**:
  - Parses command-line inputs and options (e.g., `--query <term>` or positional query argument).
  - Renders matched customer records (displaying ID, Name, and Email) in a readable format.
  - Renders user notifications when no matches are found (`No customers found matching '<term>'`).
  - Displays usage instructions and user-friendly error messages on invalid input or storage failures.
  - Manages process exit codes (`0` for success or no-match; non-zero for validation/file errors).
- **Customer Service**:
  - Validates search query inputs (ensures queries are provided and not empty/whitespace-only).
  - Performs case-insensitive partial substring matching against customer name and email fields (OR condition).
  - Maps raw data into `Customer` domain models (`id`, `name`, `email`).
  - Raises domain-specific exceptions (e.g., `ValidationError`) on invalid search parameters.
- **JSON Storage (`customers.json`)**:
  - Reads and writes `customers.json`.
  - Parses JSON content and returns structured customer records.
  - Handles file system and syntax errors (missing file, unreadable file, malformed JSON).
  - Raises storage-specific exceptions (e.g., `StorageError`) to isolate file handling from the service.

## Data Flow
1. User executes a search command via CLI (e.g., `python -m customer_search --query "smith"`).
2. CLI parses the command-line arguments and invokes `CustomerService.search(query)`.
3. Customer Service validates the query according to business rules (rejects empty or whitespace query).
4. Customer Service requests customer records from JSON Storage.
5. JSON Storage reads and parses `customers.json`.
6. JSON Storage returns customer records to Customer Service.
7. Customer Service executes case-insensitive substring search on customer name and email fields.
8. Customer Service returns matching `Customer` records (or an empty list) to CLI.
9. CLI renders the formatted results (or notification message) and terminates with exit code 0.

## Interfaces
- **CLI <-> Customer Service**:
  - `CustomerService.search(query: str) -> list[Customer]`
  - Exceptions: `ValidationError`
- **Customer Service <-> JSON Storage**:
  - `CustomerStorage.read_all() -> list[dict]`
  - `CustomerStorage.save_all(records: list[dict]) -> None`
  - Exceptions: `StorageError` (wrapping `FileNotFoundError`, `json.JSONDecodeError`, `PermissionError`)
- **Domain Model**:
  - `Customer(id: int, name: str, email: str)`
- **CLI Interface**:
  - Invocation: `python -m customer_search [OPTIONS] [QUERY]`
  - Stdout: Formatted customer records or no-match notification.
  - Stderr: Error messages and CLI usage instructions.
  - Exit codes: `0` for success, non-zero for validation or file errors.

## Error Handling
- **Input Validation**: Validation belongs to the Customer Service. If the query is empty or whitespace-only, the service raises a `ValidationError`. The CLI catches it, renders a clear error message along with CLI usage instructions to stderr, and exits with a non-zero code.
- **Storage & File I/O**: File access and JSON parsing errors belong to JSON Storage. If `customers.json` is missing, unreadable, or malformed, JSON Storage raises a `StorageError`. The CLI catches it, renders a clear file error message to stderr, and exits with a non-zero code.
- **No Matching Records**: An empty search result is treated as a valid outcome. The CLI renders `No customers found matching '<term>'` to stdout and terminates with exit code 0.

## Testing Strategy
- **Unit Tests for Service (`tests/test_service.py`)**:
  - Test query validation rules (empty, whitespace, missing).
  - Test case-insensitive substring matching on name (SR-01).
  - Test case-insensitive substring matching on email (SR-02).
  - Test OR condition matching across name and email (SR-03).
  - Verify domain logic using mock storage.
- **Persistence Tests for Storage (`tests/test_storage.py`)**:
  - Test reading and writing `customers.json` using isolated temporary directories (`tmp_path`).
  - Test handling of missing files, empty files, and malformed JSON syntax.
- **CLI Verification (`tests/test_cli.py`)**:
  - Test argument parsing (`--query` and positional arguments).
  - Test output formatting for matched records.
  - Test "no customers found" output.
  - Test error messages and exit codes (`0` vs. non-zero).
  - Performance verification: ensure search completes in <1.0s for datasets up to 100 records (NFR-01).
  - Offline verification: verify no network requests or external API calls are made (NFR-03).

## Dependencies
- **Runtime**: Python standard library only (Python 3.11+) (`argparse`, `json`, `dataclasses`, `pathlib`).
- **Development & Testing**: `pytest` for running automated unit, persistence, and CLI test suites.

## Design Decisions
- **Strict Separation of Concerns**: Keep business logic (Customer Service) completely independent from the presentation layer (CLI) and storage layer (JSON Storage) for high testability and maintainability.
- **Zero External Runtime Dependencies**: Rely solely on Python's standard library to guarantee offline execution, minimal startup overhead, and easy distribution.
- **Centralized Exception Handling in CLI**: Service and Storage raise domain-specific exceptions (`ValidationError`, `StorageError`), allowing the CLI to be the single point responsible for formatting user messages and setting process exit codes.
- **Lightweight In-Memory Search**: Read customer dataset into memory for simple, fast in-memory filtering that easily fulfills the 1.0-second performance target for datasets up to 100 records.

## Trade-offs
- **In-Memory Loading vs. Streaming/Database**:
  - *Chosen*: Load entire `customers.json` into memory.
  - *Trade-off*: Straightforward implementation meeting NFR-01 (<1.0s for 100 records), but not suited for very large datasets that exceed available system memory.
- **Linear Scan (O(N)) vs. Full-Text Indexing**:
  - *Chosen*: Linear substring matching across customer records.
  - *Trade-off*: Eliminates indexing complexity and disk overhead; scales linearly with dataset size, which is optimal for small-to-medium local datasets.
- **Standard Library `argparse` vs. Third-Party CLI Frameworks (Click/Typer)**:
  - *Chosen*: Standard library `argparse`.
  - *Trade-off*: Slightly more boilerplate code for argument parsing and formatting, but introduces zero external dependencies and ensures offline portability.