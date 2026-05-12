import multiprocessing
import time


def producer(tasks_q, num_tasks, num_consumers):
    for i in range(1, num_tasks + 1):
        tasks_q.put(i)
        print(f"[Producer] put task {i}")
        time.sleep(0.05)
    # стоп-сигналы по числу consumers
    for _ in range(num_consumers):
        tasks_q.put(None)
    print("[Producer] done")


def consumer(name, tasks_q, results_q):
    while True:
        task = tasks_q.get()
        if task is None:
            print(f"[Consumer {name}] received stop signal, exiting")
            break
        result = task * task
        time.sleep(0.2)
        results_q.put((name, task, result))
        print(f"[Consumer {name}] processed {task} -> {result}")


if __name__ == "__main__":
    # Создай tasks_q и results_q (multiprocessing.Queue)
    task_amount = 20
    task_q = multiprocessing.Queue()
    results_q = multiprocessing.Queue()
    consumer_procs = []
    cons_num = 3
    # Запусти 1 producer
    producer_proc = multiprocessing.Process(
        target=producer, args=(task_q, task_amount, cons_num)
    )
    producer_proc.start()
    # Запусти 3 consumer процесса
    for i in range(cons_num):
        process = multiprocessing.Process(
            target=consumer, args=(f"Cons {i+1}", task_q, results_q)
        )
        process.start()
        consumer_procs.append(process)
    # join всех
    producer_proc.join()
    for proc in consumer_procs:
        proc.join()
    # Собери результаты из results_q
    results = [results_q.get() for _ in range(task_amount)]
    # Напечатай: сколько результатов, кто что обработал
    consumer_dict = {f"Cons {k+1}": list() for k in range(3)}
    for name, task, result in results:
        consumer_dict[name].append(f"Task: {task}; Result: {result}")
    for key, val in consumer_dict.items():
        print(f"Key: {key}:")
        for mes in val:
            print(mes)
