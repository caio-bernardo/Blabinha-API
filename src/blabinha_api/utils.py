from typing import TypeVar


T = TypeVar("T")


def assert_ret(expr: T | None) -> T:
    """
    Assert that the expression is not None and return it.

    Args:
        expr: The expression to check.

    Returns:
        The expression if it is not None.

    Raises:
        AssertionError: If expr is None.
    """
    assert expr is not None, "Assertion Failed: Value is None"

    return expr
