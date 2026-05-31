def add(a: int | float, b: int | float) -> int | float:
    """Returns the sum of a and b."""
    return a + b


def subtract(a: int | float, b: int | float) -> int | float:
    """Returns a minus b."""
    return a - b


def divide(a: int | float, b: int | float) -> float:
    """Returns a divided by b. Raises ZeroDivisionError if b is zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":
    print(add(2, 3))
    print(subtract(10, 4))
    print(divide(10, 2))
