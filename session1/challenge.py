import timeit
import random

def bubble_sort(arr):
    n = len(arr)
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        if not swapped:
            break
    return arr

setup_code = """
from __main__ import bubble_sort
import random
arr = [random.randint(1,1000) for _ in range(1000)]
"""

time_taken = timeit.timeit(
    "bubble_sort(arr.copy())",
    setup = setup_code,
    number=10
)

average_time = time_taken / 10

print(f"Total time:, {time_taken:.4f} seconds")

print(f"Average time per run: {average_time * 1000:.3f} ms")




