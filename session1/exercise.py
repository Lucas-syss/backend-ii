import timeit

call_count = 0

def factorial(n):
    global call_count
    call_count += 1
    
    if n == 0 or n == 1:
       return 1
   
    return n * factorial(n - 1)

n = 10

call_count = 0

result = factorial(n)

print("Factorial:", result)
print("Function calls:", call_count)

time_taken = timeit.timeit(
    "factorial(n)",
    globals=globals(),
    number=10000
)

average_time = time_taken / 10000

print(f"Total time:, {time_taken:.4f} seconds")
print(f"Average time per call: {average_time * 1000:.6f} ms")
