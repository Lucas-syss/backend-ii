import threading
import time

def print_numbers():
    """Print numbers 1–5 with a short delay between each."""
    for i in range(1, 6):
        print(f"[Numbers] {i}")
        time.sleep(0.5)

def print_letters():
    """Print letters A–E with a short delay between each."""
    for letter in "ABCDE":
        print(f"[Letters] {letter}")
        time.sleep(0.5)

if __name__ == "__main__":
    t1 = threading.Thread(target=print_numbers)
    t2 = threading.Thread(target=print_letters)

    t1.start()
    t2.start()

 
    t1.join()
    t2.join()

    print("\nBoth threads finished.")