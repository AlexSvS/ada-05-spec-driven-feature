"""Domain models for customer_search."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    """Domain model representing a customer entity."""

    id: int
    name: str
    email: str
