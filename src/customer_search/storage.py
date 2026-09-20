"""Customer JSON storage persistence layer."""

import json
from pathlib import Path
from typing import Any


class StorageError(Exception):
    """Raised when customer storage encounters an I/O, parse, or integrity error."""


class CustomerStorage:
    """Handles reading and writing customer records from/to a local JSON file."""

    def __init__(self, file_path: str | Path = "customers.json") -> None:
        self.file_path = Path(file_path)

    def read_all(self) -> list[dict[str, Any]]:
        """Read all customer records from the JSON file.

        Returns:
            list[dict[str, Any]]: List of customer dictionaries.

        Raises:
            StorageError: If the file does not exist, cannot be read, contains
                invalid JSON, or contains malformed customer records.
        """
        if not self.file_path.exists():
            raise StorageError(f"Customer data file not found: '{self.file_path}'")

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except PermissionError as err:
            raise StorageError(f"Permission denied reading customer file '{self.file_path}': {err}") from err
        except (json.JSONDecodeError, UnicodeDecodeError) as err:
            raise StorageError(f"Malformed JSON in customer file '{self.file_path}': {err}") from err
        except OSError as err:
            raise StorageError(f"Error reading customer file '{self.file_path}': {err}") from err

        if not isinstance(data, list):
            raise StorageError(f"Invalid format in customer file '{self.file_path}': expected a JSON array")

        for index, record in enumerate(data):
            if not isinstance(record, dict):
                raise StorageError(
                    f"Invalid record at index {index} in '{self.file_path}': expected a JSON object"
                )
            if not all(key in record for key in ("id", "name", "email")):
                raise StorageError(
                    f"Record at index {index} in '{self.file_path}' is missing required fields (id, name, email)"
                )
            if (
                not isinstance(record["id"], int)
                or not isinstance(record["name"], str)
                or not isinstance(record["email"], str)
            ):
                raise StorageError(
                    f"Record at index {index} in '{self.file_path}' contains invalid field types"
                )

        return data

    def save_all(self, records: list[dict[str, Any]]) -> None:
        """Write customer records to the JSON file.

        Args:
            records: List of customer dictionaries to save.

        Raises:
            StorageError: If writing to the file fails.
        """
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
        except OSError as err:
            raise StorageError(f"Error writing customer file '{self.file_path}': {err}") from err
