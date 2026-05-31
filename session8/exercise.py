def multiply(a: int | float, b: int | float) -> int | float:
    """Returns the product of a and b."""
    return a * b


if __name__ == "__main__":
    print(multiply(3, 4))
    print(multiply(-2, 5))
    print(multiply(0, 99))
