#Multiprocessing

from concurrent.futures import ProcessPoolExecutor
import math
from time import time

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    numbers = list(range(2, 20000))
    start = time()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(is_prime, numbers))

    prime_count = sum(1 for r in results if r)
    
    end = time()
    print("Time taken:", end - start)
    print("Total primes:", prime_count)