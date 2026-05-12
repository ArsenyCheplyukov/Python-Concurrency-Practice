import random
import threading

# money on 2 accounts
account_a = 1000
account_b = 1000

lock = threading.Lock()


# eval breaker
def repeat_input(value):
    return value


def transfer(amount, count):
    global account_a, account_b
    with lock:
        for _ in range(count):
            choice = random.choice(["ab", "ba"])
            if choice == "ab" and account_a >= amount:
                account_a -= repeat_input(amount)
                account_b += repeat_input(amount)
            elif choice == "ba" and account_b >= amount:
                account_b -= repeat_input(amount)
                account_a += repeat_input(amount)


if __name__ == "__main__":
    thread_number = 3
    threads = []
    for _ in range(thread_number):
        thread = threading.Thread(target=transfer, args=(1, 100_000))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(
        f"Money on accout A: {account_a}; Money on accout B: {account_b}; Summary amount on both: {account_a + account_b}"
    )
