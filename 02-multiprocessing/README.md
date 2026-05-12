# 02 — Multiprocessing

Эксперименты с `multiprocessing` модулем: PID, CPU-bound speedup, Pool API, producer-consumer.

## Контекст

- В отличие от `threading`, каждый процесс имеет свой Python interpreter и свой GIL.
- Это позволяет реальный параллелизм на CPU-bound задачах.
- Цена: дорогой старт (fork + interpreter init), IPC через pickle, изолированная память.

## Файлы

- `01_basic_process.py` — `Process(target=...).start().join()`, PID/PPID, параллельный sleep × 3 ≈ 1 секунда.
- `02_cpu_speedup.py` — count primes в диапазоне. На 5-секундной задаче:
  - sequential: 5.0 с
  - threading × 10: 5.3 с (GIL держит → нет ускорения, даже overhead)
  - multiprocessing × 10: 1.3 с (× 3.87 ускорение)
  - **Доказательство:** threading бесполезен на CPU-bound, multiprocessing работает.
- `03_pool_map.py` — `Pool.starmap` для batch processing. Эквивалентно ручному Process для 4-10 задач, выигрывает на большом числе мелких задач.
- `04_producer_consumer.py` — паттерн producer/consumer через `multiprocessing.Queue` + sentinel (None) для graceful shutdown. Backbone для message queues (Celery, Kafka, SQS).

## Ключевые выводы

1. **GIL — главная причина существования multiprocessing.** На I/O threading достаточно, на CPU — только процессы.
2. **Overhead важен.** На задачах < 1 секунды multiprocessing может проиграть из-за старта процессов. Sweet spot: задачи от 1 секунды и больше.
3. **`Pool` vs ручной `Process`:** Pool побеждает на **многих** задачах (переиспользует workers). На разовых задачах ручной Process быстрее.
4. **`Queue` инкапсулирует синхронизацию.** Получаешь thread-safe буфер без явных Lock'ов.
5. **Sentinel pattern** — стандартный способ сказать consumer'ам "конец работы".

## Подводные камни

- `args=(x)` — это НЕ кортеж, а `x`. Нужно `args=(x,)`.
- `if __name__ == "__main__":` обязателен (иначе infinite recursion на Windows / некоторые fork режимы).
- Pickle constraint: lambda, локальные функции, открытые сокеты — нельзя передать в Process.
- `multiprocessing.Queue` ≠ `queue.Queue`. Первый для процессов (pickle), второй для потоков (Lock). Перепутаешь — данные тихо потеряются.
- `q.get()` блокирует пока очередь не пуста. Не используй `while not q.empty()` — race condition.

## Открытые темы (на будущее)

- `Pool.imap` / `imap_unordered` — итеративные варианты map, не ждут всех результатов сразу
- `multiprocessing.Manager` — общие dict/list между процессами через прокси
- `multiprocessing.Value` / `Array` — shared memory без pickle
- `multiprocessing.shared_memory` (3.8+) — для numpy/больших массивов
- `concurrent.futures.ProcessPoolExecutor` — современный единый API
- Pipe vs Queue — разница и когда что
- Load imbalance + chunksize в Pool.map
