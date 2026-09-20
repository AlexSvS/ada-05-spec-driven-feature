"""Customer search business logic service layer."""

from typing import Protocol

from customer_search.models import Customer
from customer_search.storage import CustomerStorage


class StorageProtocol(Protocol):
    """Protocol defining the storage interface required by CustomerService."""

    def read_all(self) -> list[dict]:
        ...


class ValidationError(Exception):
    """Raised when search query validation fails."""


class CustomerService:
    """Service handling customer search logic and business rules."""

    def __init__(self, storage: StorageProtocol | None = None) -> None:
        self.storage = storage if storage is not None else CustomerStorage()

    def search(self, query: str) -> list[Customer]:
        """Search customers by name or email with case-insensitive partial match.

        Args:
            query: The search term to match against name or email.

        Returns:
            list[Customer]: Matching customer records in encounter order.

        Raises:
            ValidationError: If the query is empty or contains only whitespace.
        """
        if query is None or not isinstance(query, str) or not query.strip():
            raise ValidationError("Search query cannot be empty or whitespace.")

        normalized_query = query.strip().lower()
        raw_records = self.storage.read_all()

        matches: list[Customer] = []
        for record in raw_records:
            customer = Customer(
                id=record["id"],
                name=record["name"],
                email=record["email"],
            )
            # SR-01, SR-02, SR-03: case-insensitive partial substring match on name OR email
            if (
                normalized_query in customer.name.lower()
                or normalized_query in customer.email.lower()
            ):
                matches.append(customer)

        return matches
