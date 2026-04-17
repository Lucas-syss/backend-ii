# Session 1: Big O Notation 📊

## What is Big O?

Big O notation is a way to describe **how an algorithm's runtime scales as the input grows**. It answers the question: *"If I double the size of my data, how much slower does my code get?"*

It's not about exact speed — it's about the **growth pattern**.

> **Simple analogy:** Imagine searching for a name in a phonebook. Flipping page by page is O(n). Opening to the middle and halving the search each time is O(log n). Opening directly to the right page is O(1).

---

## The Common Complexities

| Big O | Name | Example |
|---|---|---|
| O(1) | Constant | Dictionary lookup, list index access |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Loop through a list |
| O(n log n) | Log-linear | Merge sort, Python's built-in `sort()` |
| O(n²) | Quadratic | Nested loops, bubble sort |
| O(2ⁿ) | Exponential | Naive recursive Fibonacci |

**Rule of thumb:** the further down this table, the worse it scales. O(1) is ideal; O(2ⁿ) becomes unusable fast.

---

## The GIL — Why it matters

### O(1) — Constant time
Runtime doesn't change regardless of input size.
```python
my_list = [1, 2, 3, 4, 5]
first = my_list[0]  # Always one step, no matter how long the list
```

### O(n) — Linear time
Runtime grows proportionally with input.
```python
def linear_search(lst, target):
    for item in lst:           # Visits every element in the worst case
        if item == target:
            return True
    return False
# Double the list → double the time
```

### O(log n) — Logarithmic time
Runtime grows very slowly — each step cuts the problem in half.
```python
def binary_search(lst, target):
    low, high = 0, len(lst) - 1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
# List of 1,000,000 items → only ~20 steps!
```
> **Requires a sorted list.**

### O(n²) — Quadratic time
A loop inside a loop. Gets very slow, very fast.
```python
def has_duplicates(lst):
    for i in range(len(lst)):
        for j in range(len(lst)):   # Nested loop = n × n steps
            if i != j and lst[i] == lst[j]:
                return True
    return False
# Double the list → 4× the time
```

---

## When to Think About Big O

✅ Always consider it when:
- Working with **large datasets** (thousands+ items)
- Writing **search or sort** logic
- **Nested loops** appear in your code
- Code runs **noticeably slow** and you need to diagnose why

❌ Don't over-optimise when:
- Data is small and always will be
- Readability matters more than micro-performance
- A built-in Python function already handles it efficiently

---

## Python Built-ins and Their Complexity

| Operation | Data Structure | Complexity |
|---|---|---|
| `lst[i]` | List | O(1) |
| `lst.append(x)` | List | O(1) |
| `x in lst` | List | O(n) |
| `x in my_set` | Set | O(1) |
| `my_dict[key]` | Dict | O(1) |
| `lst.sort()` | List | O(n log n) |
| `sorted(lst)` | Any | O(n log n) |

> **Key insight:** Switching a `list` lookup to a `set` lookup changes O(n) to O(1). A simple change that can make a massive difference.

---

## Quick Reference Cheat Sheet

```
O(1)       → Direct access (dict, set, list index)
O(log n)   → Halving the problem each step (binary search)
O(n)       → One loop through all items
O(n log n) → Efficient sorts (merge sort, Python sort)
O(n²)      → Loop inside a loop
O(2ⁿ)      → Recursion that branches twice per call
```

## Common Pitfalls

1. **`x in list` is O(n)** — Use a `set` or `dict` if you're checking membership repeatedly.
2. **Concatenating strings in a loop is O(n²)** — Use `"".join(parts)` instead.
3. **Nested loops aren't always O(n²)** — If the inner loop runs a fixed number of times, it's still O(n).
4. **Big O is worst-case** — An O(n) search might find the target on the first try, but we plan for the worst.