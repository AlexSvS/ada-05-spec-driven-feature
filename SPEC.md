# Customer Search Feature

## Goal
Provide a local CLI tool to search customer records by name or email from a local JSON dataset.

## Requirements Covered
- FR-01
- FR-02
- FR-03
- FR-04
- FR-05
- FR-06
- NFR-01
- NFR-02
- NFR-03
- C-01
- C-02
- A-01


## Scope
Search customer records by name or email via CLI argument, case-insensitive substring matching against local JSON data, readable console output of matches, clear no-match notification, input validation, and proper exit code handling.

## Out of Scope
Modifying customer records (create, update, delete), web or graphical user interface, external API or network calls, multi-user authentication, and complex search queries (regex or boolean operators).

## Domain Model
Customer:
- id: int
- name: str
- email: str

Storage:
- JSON file: customers.json

## Search Rules
SR-01 [FR-02]: Query matches customer name if the query string is a case-insensitive substring of the name field.
SR-02 [FR-03]: Query matches customer email if the query string is a case-insensitive substring of the email address field.
SR-03 [FR-02, FR-03]: A customer record matches if either the name or email field contains the query substring (OR condition).
SR-04 [FR-04]: All matching customer records must be displayed with their ID, name, and email address in a readable format.
SR-05 [FR-05]: When no records match the query, display notification message: "No customers found matching '<term>'".

## Validation Rules
VR-01 [FR-01, FR-06]: Search query is required via command-line argument.
VR-02 [FR-06]: Search query cannot be empty or consist solely of whitespace.
VR-03 [A-01, NFR-02]: Customer data file must exist, be accessible, and contain valid JSON customer records.

## Error Handling
EH-01 [FR-06, NFR-02]: Missing or empty/whitespace query displays an error message with CLI usage instructions and exits with a non-zero exit code.
EH-02 [NFR-02, A-01]: Missing, unreadable, or malformed customer JSON file displays a clear file error message and exits with a non-zero exit code.
EH-03 [NFR-02]: Successful search execution (records displayed or no-match message displayed) terminates with exit code 0.

## Acceptance Criteria
AC-01 [FR-01]: CLI accepts a search query string via command-line argument.
AC-02 [FR-02]: Searching with a partial, case-insensitive substring of a name returns matching customer records.
AC-03 [FR-03]: Searching with a partial, case-insensitive substring of an email returns matching customer records.
AC-04 [FR-04]: Output displays all matching customer records showing ID, name, and email in a readable format.
AC-05 [FR-05, NFR-02]: When no records match, display "No customers found matching '<term>'" and exit with code 0.
AC-06 [FR-06, NFR-02]: When query is missing or empty, display error with usage instructions and exit with non-zero code.
AC-07 [NFR-01]: For a dataset containing up to 100 valid customer records, the CLI shall complete the entire search operation, including reading the JSON file and displaying the results, within 1.0 second under the defined test environment.
AC-08 [NFR-02, A-01]: Inaccessible or malformed JSON file displays an error message and exits with non-zero code.
AC-09 [NFR-03, C-01, C-02]: Search executes completely offline without external network or API calls, compatible with Python 3.11+ and pytest.

## Test Scenarios
TS-01 -> AC-01, AC-02 | TS-02 -> AC-01, AC-03 | TS-03 -> AC-04
TS-04 -> AC-05        | TS-05 -> VR-01/EH-01  | TS-06 -> VR-02/EH-01
TS-07 -> AC-07        | TS-08 -> VR-03/EH-02, A-01 | TS-09 -> AC-09, C-01, C-02

## Constraints
C-01 [C-01]: Local CLI tool execution only; external web services, APIs, or network requests are prohibited.
C-02 [C-02]: Implementation language must be Python 3.11+, and test suite must use pytest.
A-01 [A-01]: Customer dataset is stored in a local JSON file that is accessible by the CLI and fits within available system memory.

## Open Questions
OQ-01 [Q-01]: Acceptance of defaulting strictly to local `customers.json`.
OQ-02 [Q-02]: Result ordering strategy by dataset encounter order