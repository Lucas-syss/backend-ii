def factorial(n):
    """Recursively compute n! (n factorial)."""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

for i in range(6):
    print(f"{i}! = {factorial(i)}")