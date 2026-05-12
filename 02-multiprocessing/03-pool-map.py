import multiprocessing
from time import perf_counter


def count_primes_in_range(start, end):
    count = 0
    for n in range(start, end):
        if n < 2:
            continue
        is_prime = True
        for d in range(2, int(n**0.5) + 1):
            if n % d == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count


if __name__ == "__main__":
    val_ranges = [
        (2, 500_000),
        (500_000, 1000_000),
        (1000_000, 1500_000),
        (1500_000, 2000_000),
    ]
    start_time = perf_counter()
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.starmap(count_primes_in_range, val_ranges)
    print(
        f"Result is: {sum(results)}. Execution time is: {perf_counter() - start_time}"
    )
