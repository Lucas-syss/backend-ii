def factorial(n: int) -> int:
    """Returns n! recursively. Raises ValueError for negative inputs."""
    if n < 0:
        raise ValueError(f"Factorial is not defined for negative numbers, got {n}")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


if __name__ == "__main__":
    for i in range(8):
        print(f"{i}! = {factorial(i)}")
