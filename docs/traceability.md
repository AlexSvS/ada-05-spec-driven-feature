# Requirements Traceability Matrix

| Requirement | SPEC/AC | Task | Files | Test | Status | Notes |
|-------------|---------|------|-------|------|--------|-------|
| FR-01 | AC-01, VR-01 | T-03, T-04 | `src/customer_search/cli.py` | `test_cli_presentation_with_flag`, `test_cli_presentation_with_positional` | PASSED | Supports `-q`/`--query` flag and positional argument |
| FR-02 | AC-02, SR-01 | T-03 | `src/customer_search/service.py` | `test_search_partial_name_match`, `test_search_name_case_insensitivity` | PASSED | Case-insensitive partial name substring matching |
| FR-03 | AC-03, SR-02 | T-03 | `src/customer_search/service.py` | `test_search_partial_email_match`, `test_search_email_case_insensitivity` | PASSED | Case-insensitive partial email substring matching |
| FR-04 | AC-04, SR-04 | T-03 | `src/customer_search/cli.py` | `test_format_customer_output`, `test_cli_presentation_with_flag`, `test_cli_presentation_with_positional` | PASSED | Formats records with ID, Name, and Email |
| FR-05 | AC-05, SR-05 | T-03 | `src/customer_search/cli.py` | `test_cli_no_match_notification`, `test_success_exit_code_without_matches` | PASSED | Displays `No customers found matching '<term>'` on no matches |
| FR-06 | AC-06, VR-01, VR-02, EH-01 | T-04 | `src/customer_search/cli.py`, `src/customer_search/service.py` | `test_validation_error_missing_query_positional`, `test_validation_error_empty_string_query`, `test_validation_error_whitespace_query`, `test_validation_error_empty_query_flag` | PASSED | Error message and CLI usage instructions printed to stderr |
| NFR-01 | AC-07 | T-05 | `src/customer_search/cli.py`, `src/customer_search/service.py` | `test_performance_benchmark_hundred_records` | PASSED | Search on 100 customer records completes well under 1.0s limit |
| NFR-02 | EH-01, EH-02, EH-03 | T-04 | `src/customer_search/cli.py` | `test_success_exit_code_with_matches`, `test_success_exit_code_without_matches`, `test_validation_error_missing_query_positional`, `test_storage_error_missing_file`, `test_storage_error_malformed_json_file` | PASSED | Exit code 0 for success, 1 for validation error, 2 for storage error |
| NFR-03 | AC-09 | T-01, T-05 | `pyproject.toml`, `src/customer_search/` | `test_offline_execution_prohibits_network`, `test_no_external_dependencies` | PASSED | 100% offline execution; zero external network/API calls |
| C-01 | AC-09 | T-01, T-05 | `src/customer_search/` | `test_offline_execution_prohibits_network`, `test_subprocess_success_exit_code` | PASSED | Fully local CLI tool execution without remote services |
| C-02 | AC-09 | T-01, T-05 | `pyproject.toml` | `test_python_version` | PASSED | Python 3.11+ runtime verified and tested with pytest |
| A-01 | VR-03, EH-02 | T-01, T-02 | `customers.json`, `src/customer_search/storage.py` | `test_customers_json_exists_and_valid`, `test_read_all_valid_records`, `test_read_all_default_customers_file` | PASSED | Customer dataset stored in local `customers.json` |