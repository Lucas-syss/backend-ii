import multiprocessing

def factorial(n):
    """Recursive factorial function."""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def compute_and_print_factorial(n):
    """Wrapper that computes and prints the result."""
    result = factorial(n)
    print(f"Factorial of {n} = {result}")

if __name__ == "__main__":
    numbers = [5, 7, 10, 12, 15]
    processes = []

    # Spawn one process per number
    for number in numbers:
        p = multiprocessing.Process(target=compute_and_print_factorial, args=(number,))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("All factorial computations complete.")