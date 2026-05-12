import sys
import threading

counter = 0


def one():
    return 1


def increment():
    global counter
    for _ in range(100_000):
        counter += one()  # ← function call = eval breaker


if __name__ == "__main__":
    sys.setswitchinterval(0.000001)
    threads = []
    for _ in range(4):
        thread = threading.Thread(target=increment, args=())
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(counter)
