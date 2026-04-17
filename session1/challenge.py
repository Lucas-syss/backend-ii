def bubble_sort_optimised(lst):
    """
    Optimised bubble sort that exits early if no swaps occurred in a pass,
    meaning the list is already sorted.
    """
    n = len(lst)

    for i in range(n):
        swapped = False  

        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                swapped = True  

        if not swapped:
            print(f"  Early exit after {i + 1} pass(es)!")
            break

    return lst


print("Test 1: Already sorted")
result = bubble_sort_optimised([1, 2, 3, 4, 5])
print(result)

print("\nTest 2: Reverse sorted (worst case)")
result = bubble_sort_optimised([5, 4, 3, 2, 1])
print(result)

print("\nTest 3: Nearly sorted")
result = bubble_sort_optimised([1, 2, 4, 3, 5])
print(result)

print("\nTest 4: Random order")
result = bubble_sort_optimised([64, 34, 25, 12, 22, 11, 90])
print(result)