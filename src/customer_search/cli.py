"""CLI presentation layer for customer search."""

import argparse
import sys

from customer_search.models import Customer
from customer_search.service import CustomerService, ValidationError
from customer_search.storage import CustomerStorage, StorageError


def format_customer(customer: Customer) -> str:
    """Format a Customer record for readable console display."""
    return f"ID: {customer.id} | Name: {customer.name} | Email: {customer.email}"


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="customer_search",
        description="Search customer records by name or email.",
    )
    parser.add_argument(
        "positional_query",
        nargs="?",
        default=None,
        metavar="QUERY",
        help="Search query term (name or email substring)",
    )
    parser.add_argument(
        "-q",
        "--query",
        dest="flag_query",
        default=None,
        help="Search query term (name or email substring)",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="file_path",
        default="customers.json",
        help="Path to customer JSON data file (default: customers.json)",
    )
    return parser


def main(
    argv: list[str] | None = None,
    service: CustomerService | None = None,
    storage: CustomerStorage | None = None,
) -> int:
    """Main CLI entrypoint.

    Args:
        argv: Optional list of command-line arguments. Defaults to sys.argv[1:].
        service: Optional CustomerService instance for dependency injection.
        storage: Optional CustomerStorage instance for dependency injection.

    Returns:
        int: Process exit code (0 for success, non-zero for errors).
    """
    parser = create_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    # Prefer flag if explicitly provided, else positional
    query = args.flag_query if args.flag_query is not None else args.positional_query

    # VR-01, EH-01: Missing query argument displays error and CLI usage
    if query is None:
        sys.stderr.write("Error: Search query is required.\n")
        parser.print_usage(sys.stderr)
        return 1

    if service is None:
        if storage is None:
            storage = CustomerStorage(file_path=args.file_path)
        service = CustomerService(storage=storage)

    try:
        # VR-02, EH-01: Empty or whitespace query will raise ValidationError
        results = service.search(query)
    except ValidationError as err:
        sys.stderr.write(f"Validation Error: {err}\n")
        parser.print_usage(sys.stderr)
        return 1
    except StorageError as err:
        # EH-02: Missing, unreadable, or malformed customer JSON file
        sys.stderr.write(f"Storage Error: {err}\n")
        return 2

    # EH-03: Successful execution returns exit code 0
    if not results:
        print(f"No customers found matching '{query}'")
    else:
        for customer in results:
            print(format_customer(customer))

    return 0
