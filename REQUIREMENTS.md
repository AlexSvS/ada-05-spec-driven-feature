# Requirements — Customer Search

## User Story
As a user,
I want to search customers by name or email,
so that I can quickly find the customer record I need.

## Functional Requirements
FR-01: The CLI shall accept a search query string via a command-line argument (e.g., `--query <term>` or positional argument).
FR-02: The system shall perform a partial, case-insensitive substring match against customer name fields.
FR-03: The system shall perform a partial, case-insensitive substring match against customer email address fields.
FR-04: The system shall output all matching customer records displaying their ID, name, and email address in a readable format.
FR-05: The system shall display a clear notification message (e.g., "No customers found matching '<term>'") when no records match.
FR-06: The system shall validate input and display an error message with CLI usage instructions if the query string is empty or missing.

## Non-Functional Requirements
NFR-01: The CLI shall return search results within 1.0 second for datasets of up to 100 local customer records.
NFR-02: The CLI shall return an exit code of 0 on successful search execution and a non-zero exit code on invalid arguments or file access errors.
NFR-03: The application shall run entirely offline on the local machine with no external API calls or network dependencies.

## Open Questions
Q-01: Should the CLI accept a custom path to the customer JSON file via a flag (e.g., `--file <path>`), or default to a standard local file (e.g., `customers.json`)?
Q-02: How should results be ordered (e.g., alphabetical by name, ID, or match relevance), and should there be a maximum display limit?

## Constraints / Assumptions
C-01: Must be implemented as a local CLI tool without using any external web services or APIs.
C-02: Must be implemented using Python 3.11+ and pytest.
A-01: Customer dataset is stored in a local JSON file that is accessible by the CLI and fits within available system memory.
