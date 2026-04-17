import multiprocessing

def sum_of_squares(sublist):
    """Compute the sum of squares for a given sublist."""
    result = sum(x ** 2 for x in sublist)
    print(f"Sum of squares for {sublist} = {result}")
    return result

def divide_into_chunks(lst, chunk_size):
    """Split a list into sublists of a given size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

if __name__ == "__main__":

    numbers = list(range(1, 25))  
    chunk_size = 6

    sublists = divide_into_chunks(numbers, chunk_size)
    print(f"Sublists: {sublists}\n")

    with multiprocessing.Pool() as pool:
        results = pool.map(sum_of_squares, sublists)

    print(f"\nIndividual sums of squares: {results}")
    print(f"Grand total: {sum(results)}")