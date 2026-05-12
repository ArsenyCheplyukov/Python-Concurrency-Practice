import multiprocessing
import os
import time


def worker(name):
    print(f"Worker {name} started, PID={os.getpid()}, parent PID={os.getppid()}")
    time.sleep(1)
    print(f"Worker {name} finished")


if __name__ == "__main__":
    print(f"Main PID={os.getpid()}")
    processes = []
    for name in ("A", "B", "C"):
        process = multiprocessing.Process(target=worker, args=(name,))
        processes.append(process)
        process.start()

    for proc in processes:
        proc.join()

    print("All workers done")
