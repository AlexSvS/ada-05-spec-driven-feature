# Agent Report

## Agent / Version
Antigravity CLI / Gemini 3.8 Flash (High)

## Initial Context
The repository contained the foundational project documentation (`REQUIREMENTS.md`, `SPEC.md`, `ARQUITECTURE.md`, `TASKS.md`, `AGENTS.md`) and empty `src/` and `tests/` directories. The goal was to incrementally implement the Customer Search feature following specification-driven development rules without modifying requirements or inventing business rules.

## Task Sequence

### T-01 Project Setup
- **What the agent did**: Configured `pyproject.toml` with Python 3.11+ requirement, zero external runtime dependencies, and pytest discovery; initialized `src/customer_search/__init__.py` and `tests/__init__.py`; created `customers.json` conforming to domain schema; created `tests/test_setup.py`.
- **Human review**: The student manually reviewed the setup code (customer.json that stores the default customers, pyproject.toml that demostrates the lack of external dependencies and test_setup.py that tests if the project only works locally and with Python, pytest and without external API's). The student accepted the results due to the satisfaction of C-01, C-02, NFR-03, and AC-09.
- **Tests**: `tests/test_setup.py` (4 passed).
    - test_python_version
    - test_package_import
    - test_customers_json_exists_and_valid
    - test_no_external_dependencies

### T-02 Domain Model
- **What the agent did**: Implemented `Customer` dataclass in `src/customer_search/models.py`; implemented `CustomerStorage` persistence layer and `StorageError` exception in `src/customer_search/storage.py` handling file I/O and JSON parsing; added comprehensive persistence tests in `tests/test_storage.py`.
- **Human review**: The student manually reviewed the code (models.py that contains the correct atributes of the object Customer, storage.py that handles the reads/writes and errors in the JSON file, test_storage.py that tests the persistance of the storage) and accepted the results due to the satisfaction of A-01, VR-03, EH-02, AC-08, TS-08.
- **Tests**: `tests/test_storage.py` (10 passed; 14 total).
    - test_customer_model_instantiation
    - test_read_all_valid_records
    - test_read_all_default_customers_file
    - test_read_all_missing_file
    - test_read_all_empty_file
    - test_read_all_malformed_json_syntax
    - test_read_all_not_a_list
    - test_read_all_record_missing_field
    - test_read_all_record_invalid_field_type
    - test_save_all_and_read_back

### T-03 Search Logic
- **What the agent did**: Implemented `CustomerService` in `src/customer_search/service.py` performing case-insensitive partial substring search across customer names and emails (OR condition) preserving encounter order; implemented CLI presentation layer in `src/customer_search/cli.py` formatting matched records or no-match message; created entrypoint in `src/customer_search/__main__.py`.
- **Human review**: The student manually reviewed each code and accepted the results due to the pass of FR-01, FR-02, FR-03, FR-04, FR-05, SR-01, SR-02, SR-03, SR-04, SR-05, AC-01, AC-02, AC-03, AC-04, and AC-05.
- **Tests**: `tests/test_service.py` (11 passed; 25 total) and manual CLI verification.
    - test_search_partial_name_match
    - test_search_name_case_insensitivity    
    - test_search_partial_email_match
    - test_search_email_case_insensitivity
    - test_search_or_condition    
    - test_search_no_match_returns_empty_list    
    - test_search_preserves_encounter_order
    - test_format_customer_output
    - test_cli_presentation_with_flag
    - test_cli_presentation_with_positional    
    - test_cli_no_match_notification

### T-04 Validation and Errors
- **What the agent did**: Refined CLI and service query validation to reject missing, empty, or whitespace queries with usage instructions printed to `stderr`; mapped errors to standard process exit codes (0 for success, 1 for validation error, 2 for storage error); supported configurable `--file` argument; added comprehensive CLI tests in `tests/test_cli.py`.
- **Human review**: The student manually reviewed the code and was aided by an agent (ChatGPT) to check if test_cli.py and test_storage have duplicated tests between each other. It was discovered that, although both file verify similar behaviors, they do it in different layers (CLI interface and storage layer). After this, the student accepted the results since they satisfy FR-06, VR-01, VR-02, EH-01, EH-02, EH-03, AC-06, and NFR-02.
- **Tests**: `tests/test_cli.py -k "validation or error"` (7 passed; 35 total).
    - test_validation_error_missing_query_positional    
    - test_validation_error_empty_string_query
    - test_validation_error_whitespace_query
    - test_validation_error_empty_query_flag
    - test_storage_error_missing_file
    - test_storage_error_malformed_json_file
    - test_subprocess_validation_error_missing_query

### T-05 Tests
- **What the agent did**: Implemented shared fixtures in `tests/conftest.py` including a 100-record dataset generator and an offline network socket blocker; implemented performance benchmark test verifying search completes in <1.0s for 100 records (NFR-01, AC-07); implemented offline execution test (NFR-03, AC-09); added Unicode support and nested directory tests in `tests/test_storage.py`.
- **Human review**: The student manually reviewed the code and accepted the results due to the satisfaction of TS-01 through TS-09, NFR-01, NFR-03, AC-07, and AC-09.
- **Tests**: Full test suite with 41 tests passing across TS-01 through TS-09.
    - test_performance_benchmark_hundred_records
    - test_offline_execution_prohibits_network
    - test_service_validation_empty_query 
    - test_service_validation_whitespace_query
    - test_storage_unicode_support
    - test_storage_save_creates_nested_directories


### T-06 Documentation
- **What the agent did**: Completed requirements traceability matrix in `docs/traceability.md` covering all requirements (FR-01–FR-06, NFR-01–NFR-03, C-01, C-02, A-01); authored comprehensive `README.md`; updated `AI-USAGE-LOG.md`; completed `results/agent-report.md`.
- **Human review**: The student did a final review of all project artifacts and documentation.
- **Tests**: Documentation review and traceability audit.

## Problems Encountered
1. `pytest` command not directly available in global PowerShell environment path: Resolved by invoking `python -m pytest`, which reliably targets the active Python 3.14 environment.
2. Initial import of `CustomerStorage` missing in `cli.py` during T-04 refactoring: Caught immediately during pytest execution, diagnosed from test traceback, and corrected.

## Human Interventions
The user reviewed each task incrementally and provided explicit approval to proceed with subsequent tasks.

## Requirement / Specification Changes
None. The implementation strictly adhered to `REQUIREMENTS.md` and `SPEC.md` without modifying requirements or inventing business behavior.

## Final Verification
- Full pytest test suite: 41 passed in 0.46s.
- 100% test scenario coverage: TS-01 through TS-09 verified.
- Traceability matrix: Complete mapping for FR-01 through FR-06, NFR-01 through NFR-03, C-01, C-02, and A-01.
- Offline execution and performance constraints fully verified.

## Lessons Learned
- Maintaining strict separation of concerns across presentation, domain logic, and persistence made writing unit tests with mock storage clean and frictionless.
- Implementing test scenarios incrementally alongside each task prevented regression bugs and maintained a continuously passing test suite throughout development.
- Separating the human review to each task prevented confusion and allowed to check each part of the application in more depth.