# Tasks

## T-01 Project setup
- Goal: Create project directory structure, configure Python 3.11+ environment, and set up pytest framework.
- Files: pyproject.toml, src/customer_search/__init__.py, tests/__init__.py, customers.json
- Acceptance: C-01, C-02, NFR-03, and AC-09 are satisfied.
- Verification: pytest -v

## T-02 Domain model
- Goal: Implement Customer domain model and JSON storage persistence layer for reading and writing customers.json.
- Files: src/customer_search/models.py, src/customer_search/storage.py, customers.json, tests/test_storage.py
- Acceptance: A-01, VR-03, EH-02, and AC-08 are satisfied.
- Verification: persistence tests pass (pytest tests/test_storage.py).

## T-03 Search logic
- Goal: Implement CustomerService search logic (case-insensitive substring match on name/email) and CLI presentation for customer search queries.
- Files: src/customer_search/service.py, src/customer_search/cli.py, src/customer_search/__main__.py, tests/test_service.py
- Acceptance: FR-01, FR-02, FR-03, FR-04, FR-05, SR-01, SR-02, SR-03, SR-04, SR-05, AC-01, AC-02, AC-03, AC-04, and AC-05 pass.
- Verification: service tests pass (pytest tests/test_service.py) and manual CLI execution.

## T-04 Validation and errors
- Goal: Implement input query validation, CLI usage instructions, file error handling, and process exit code management.
- Files: src/customer_search/service.py, src/customer_search/storage.py, src/customer_search/cli.py, tests/test_cli.py
- Acceptance: FR-06, VR-01, VR-02, EH-01, EH-02, EH-03, AC-06, and NFR-02 pass.
- Verification: validation and error handling tests pass (pytest tests/test_cli.py -k "validation or error").

## T-05 Tests
- Goal: Implement comprehensive automated test suite verifying test scenarios, performance benchmark (<1.0s), and offline execution.
- Files: tests/test_service.py, tests/test_storage.py, tests/test_cli.py, tests/conftest.py
- Acceptance: TS-01 through TS-09, NFR-01, NFR-03, AC-07, and AC-09 are satisfied.
- Verification: pytest -v

## T-06 Documentation
- Goal: Update requirements traceability matrix, AI usage log, and project documentation.
- Files: AI-USAGE-LOG.md, README.md, docs/
- Acceptance: Traceability matrix complete for all requirements (FR-01–FR-06, NFR-01–NFR-03, C-01, C-02, A-01) and DoD documentation items are complete.
- Verification: documentation review and traceability audit.