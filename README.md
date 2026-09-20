# Customer Search CLI

A modular, offline command-line interface tool developed in Python 3.11+ to search customer records by name or email from a local JSON dataset.

## Features

- **Case-Insensitive Search**: Partial substring matching against customer names and email addresses (OR condition).
- **Flexible CLI Arguments**: Supports both positional queries (`python -m customer_search "smith"`) and flagged queries (`python -m customer_search --query "smith"`).
- **Custom Dataset Path**: Accepts custom customer JSON files via `--file <path>` (defaults to `customers.json`).
- **Readable Display**: Formats matching records with ID, Name, and Email.
- **Clear Notifications**: Informs user when no customer records match the query.
- **Robust Error Handling**: Centralized input validation and file I/O error handling with standard process exit codes.
- **Zero External Dependencies**: Implemented using the Python standard library only, running 100% offline.
- **High Performance**: In-memory scan completing well within 1.0 second for 100 records.

## Architecture

The project follows a 3-tier layered architecture:
1. **CLI (Presentation Layer)** (`src/customer_search/cli.py`): Parses command-line inputs, formats results or error messages to console streams (`stdout`/`stderr`), and returns exit codes.
2. **Customer Service (Business Logic Layer)** (`src/customer_search/service.py`): Validates search queries, executes case-insensitive substring search across `Customer.name` and `Customer.email`, and preserves encounter ordering.
3. **JSON Storage (Data Persistence Layer)** (`src/customer_search/storage.py`): Reads and writes local JSON files (`customers.json`), handling JSON parsing, I/O errors, and record integrity.

## Installation & Setup
Download the ZIP or clone the repository in https://github.com/AlexSvS/ada-05-spec-driven-feature.git

### Prerequisites
- Python 3.11 or higher
- pytest (for running tests)

### Local Setup
Clone the repository and install the package in editable mode:
```bash
pip install -e .
```

## Usage

### Search by Name or Email (Positional)
```bash
python -m customer_search "smith"
```
Output:
```
ID: 1 | Name: John Smith | Email: john.smith@example.com
ID: 4 | Name: Alice Smith | Email: alice.smith@domain.org
```

### Search with Flag
```bash
python -m customer_search --query "jane"
# or
python -m customer_search -q "jane"
```
Output:
```
ID: 2 | Name: Jane Doe | Email: jane.doe@example.com
```

### Search with Custom JSON File
```bash
python -m customer_search --file /path/to/custom_customers.json "smith"
```

### When No Records Match
```bash
python -m customer_search "xyz123"
```
Output:
```
No customers found matching 'xyz123'
```

### Exit Codes
- `0`: Successful execution (records displayed or no-match message displayed).
- `1`: Invalid arguments or query validation error (missing query, empty string, or whitespace-only query). Usage instructions printed to `stderr`.
- `2`: Storage or file access error (file not found, unreadable file, malformed JSON). Clear error message printed to `stderr`.

## Testing

Run the automated test suite with pytest:
```bash
pytest -v
```

Run specific test modules:
```bash
# Service logic tests
pytest tests/test_service.py -v

# Storage persistence tests
pytest tests/test_storage.py -v

# CLI and error handling tests
pytest tests/test_cli.py -v

# Validation and error tests
pytest tests/test_cli.py -k "validation or error" -v
```

## Traceability & Documentation

Detailed traceability from requirements to specification rules, architecture, tasks, and tests can be found in:
- [REQUIREMENTS.md](REQUIREMENTS.md)
- [SPEC.md](SPEC.md)
- [ARQUITECTURE.md](ARQUITECTURE.md)
- [TASKS.md](TASKS.md)
- [docs/traceability.md](docs/traceability.md)
- [AI-USAGE-LOG.md](AI-USAGE-LOG.md)
