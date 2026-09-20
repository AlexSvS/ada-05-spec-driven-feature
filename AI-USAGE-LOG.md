### Entry 01 — Customer Search Requirements Definition

Tool: Antigravity / Gemini
Date: 2026-09-19
Stage: Requirements

Prompt:
"Make the REQUIREMENTS.md file for a Customer Search function that allows searching for customers by name or email address. It must support partial search. It must be implemented as a local CLI. The requirements can be simple and brief but need to be specified in a way that they can be verified/validated. Do not use any API's."

AI contribution:
Drafted REQUIREMENTS.md adhering to the provided template, establishing verifiable functional requirements (FR-01 through FR-06 for CLI argument handling, case-insensitive partial search on name and email, output display, and error handling), non-functional requirements (NFR-01 through NFR-03 for performance, exit codes, and offline execution), open questions (Q-01, Q-02), and constraints/assumptions (C-01, A-01). 

Student decision:
The student accepted the result except for the result in Q-01. For Q-01, the question was formulated around what format should be used for storing the local customer data (e.g., JSON, CSV, or SQLite) but the student already decided on storing the data in a JSON format so the question had to be modified.

The student also has to add a constraint so the Customer Search function can be implemented using only Python and pytest.

Impact:
Updated REQUIREMENTS.md.

### Entry 02 — Customer Search Specification Definition

Tool: Antigravity / Gemini
Date: 2026-09-19
Stage: Specification

Prompt:
"Read only the REQUIREMENTS.md and from it edit the SPEC.md. The SPEC.md is the source of truth for the verifiable behavior of the feature. All requirements should be verifiable, and be transformed into into scope, rules, validations, acceptance criteria, and test scenarios that can be traced back to them. Do not write the requirements again, just reference them."

AI contribution:
Analyzed REQUIREMENTS.md. Defined verifiable scope and out-of-scope boundaries, domain model, search rules (SR-01 through SR-05), validation rules (VR-01 through VR-03), error handling specifications (EH-01 through EH-03), acceptance criteria (AC-01 through AC-09), test scenario mappings (TS-01 through TS-09), constraints (C-01, C-02, A-01), and open questions (OQ-01, OQ-02), ensuring complete traceability back to FR-01–FR-06, NFR-01–NFR-03, C-01, C-02, and A-01 without duplicating requirement text.


Student decision:
The student accepted the results and specified the JSON file to be used for storage of customer data (customers.json).

Impact:
Modified SPEC.md.

### Entry 03 — Customer Search Architecture Definition

Tool: Antigravity / Gemini
Date: 2026-09-19
Stage: Architecture

Prompt:
"Read only REQUIREMENTS.md and SPEC.md, analyze them and from them make ARQUITECTURE.md with the sections provided in the file. The arquitecture must be:
- CLI: It interprets commands and presents results.
- Customer Service: It applies business rules and validations.
- JSON Storage (customers.json): It reads and writes customers.json.
Here's a small example you can follow (NOTE: some sections don't match the ones in the file, do not modify the sections in the file)..."

AI contribution:
Analyzed REQUIREMENTS.md and SPEC.md to populate ARQUITECTURE.md preserving all pre-existing section headers (Overview, Components, Responsibilities, Data Flow, Interfaces, Error Handling, Testing Strategy, Dependencies, Design Decisions, Trade-offs). Formulated a 3-tier modular architecture comprising CLI (Presentation Layer), Customer Service (Business Logic Layer), and JSON Storage (Data Persistence Layer for customers.json). Defined complete component responsibilities, end-to-end data flow, interface contracts, error handling patterns, testing strategies aligned with specification test scenarios (TS-01 through TS-09), dependencies (Python standard library + pytest), and architectural trade-offs.

Student decision:
Accepted the generated architectural design adhering strictly to the predefined file sections, the 3-component structure (CLI, Customer Service, JSON Storage), and the offline Python 3.11+ / pytest requirements.

Impact:
Created and modified ARQUITECTURE.md.

### Entry 04 — Customer Search Tasks Definition

Tool: Antigravity / Gemini
Date: 2026-09-20
Stage: Tasks

Prompt:
"Read only REQUIREMENTS.md, SPEC.md and ARQUITECTURE.md and from them make the TASKS.md. All requirements must be traceable to at least one task, do not write them again, just reference them. Here's an example from another project to help you:
# Tasks
## T-01 Project Setup
Goal: Create project structure.
Files: src/, tests/, docs/, results/
Acceptance: pytest can execute.
Verification: pytest -v
[...]"

AI contribution:
Analyzed REQUIREMENTS.md, SPEC.md, and ARQUITECTURE.md to populate TASKS.md following the predefined task template (T-01 through T-06). Defined Goal, Files, Acceptance criteria, and Verification steps for each task. Maintained complete traceability by directly referencing all requirements (FR-01 through FR-06, NFR-01 through NFR-03, C-01, C-02, A-01), specification rules (SR-01–SR-05, VR-01–VR-03, EH-01–EH-03), acceptance criteria (AC-01–AC-09), and test scenarios (TS-01–TS-09) without duplicating requirement text.

Student decision:
The student reviewed and accepted the generated task list and traceability mappings.

Impact:
Updated TASKS.md.
