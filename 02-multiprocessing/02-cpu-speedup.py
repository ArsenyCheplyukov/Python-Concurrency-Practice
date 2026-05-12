import multiprocessing
import queue
import threading
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


def worker_proc(start, end, q):
    result = count_primes_in_range(start, end)
    q.put(result)


if __name__ == "__main__":
    # try run count prime sequentially and count it's time
    start_time = perf_counter()
    count = count_primes_in_range(2, 2_000_000)
    print(
        f"Execution of sequential search of primes: {perf_counter() - start_time}. Result is: {count}"
    )

    val_ranges = (
        (2, 200_000),
        (200_000, 400_000),
        (400_000, 600_000),
        (600_000, 800_000),
        (800_000, 1_000_000),
        (1_000_000, 1_200_000),
        (1_200_000, 1_400_000),
        (1_400_000, 1_600_000),
        (1_600_000, 1_800_000),
        (1_800_000, 2_000_000),
    )

    threads = []
    thread_res_q = queue.Queue()
    start_time = perf_counter()
    for range_start, range_end in val_ranges:
        thread = threading.Thread(
            target=worker_proc, args=(range_start, range_end, thread_res_q)
        )
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    thread_total = sum(thread_res_q.get() for _ in range(len(val_ranges)))
    print(
        f"Threads are finished. It takes: {perf_counter() - start_time}. Result is: {thread_total}"
    )

    start_time = perf_counter()
    proc_res_q = multiprocessing.Queue()
    processes = []
    for range_start, range_end in val_ranges:
        process = multiprocessing.Process(
            target=worker_proc, args=(range_start, range_end, proc_res_q)
        )
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    proc_total = sum(proc_res_q.get() for _ in range(len(val_ranges)))
    print(
        f"Processes are finished. It takes: {perf_counter() - start_time}. Total: {proc_total}"
    )
