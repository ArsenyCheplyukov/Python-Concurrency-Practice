# 03 — Asyncio

Кооперативная конкурентность через event loop: один поток, тысячи корутин.

## Контекст

- В отличие от threading/multiprocessing, asyncio — **не параллелизм**.
- Один поток, один GIL, одно процессорное ядро.
- Корутины **уступают** друг другу через `await` когда встречают ожидание (I/O, sleep, lock).
- Ниша: I/O-bound задачи с **большим** числом одновременных операций (HTTP-сервер, web scraper, чат).

## Файлы

- `01_coroutine_basics.py` — `async def`, `asyncio.run`, разница между coroutine object и выполнением. Warning про `coroutine was never awaited` — критический сигнал, не косметика.
- `02_sequential_vs_gather.py` — три `asyncio.sleep(1)` подряд vs через `gather`. Sequential: 3 сек. Gather: 1 сек. Visual proof event loop в работе.
- `03_real_io_speedup.py` — 10 HTTP запросов к httpbin.org/delay/1 тремя способами:
  - sync (requests): 31.8 с
  - threading (requests + threads): 5.1 с (× 6.2)
  - async (aiohttp + gather): 3.2 с (× 9.8)
  - **Threading и asyncio дают сопоставимое ускорение на 10 запросах. На 10000 asyncio выигрывает по памяти и накладным.**

## Ключевые выводы

1. **`await` уступает event loop'у только если awaitable не готов.** На синхронной корутине без I/O `await` ничего не переключает — выполнение линейное.
2. **`asyncio.sleep` ≠ `time.sleep`.** Первая уступает event loop'у. Вторая блокирует поток и убивает всё преимущество async.
3. **Не смешивай sync и async.** Один блокирующий вызов в `async def` (requests.get, time.sleep, psycopg2) замораживает весь event loop — других запросов не будет.
4. **Threading на I/O работает.** GIL отпускается на syscall — потоки реально параллелятся в ожидании сети. Asyncio выигрывает на масштабе, не на единичных запросах.
5. **ClientSession переиспользует TCP-соединения.** Один session на весь run, не на каждый запрос.

## Подводные камни

- `coroutine object` без запуска → потерянная работа + RuntimeWarning.
- `time.sleep` в async коде → ловушка для джунов, ломает event loop.
- `requests` в async коде → то же самое, async деградирует в sync.
- Создание новой `ClientSession` на каждый запрос → теряется connection pooling, latency растёт.

## Открытые темы (на будущее)

- `asyncio.create_task` — fire-and-forget, отличие от `await`
- `asyncio.wait` vs `asyncio.gather` vs `as_completed`
- `asyncio.Lock` / `Semaphore` / `Queue`
- Exception handling в `gather` (`return_exceptions=True`)
- Cancellation (`task.cancel()`, `CancelledError`)
- `asyncio.run_in_executor` — мост к sync коду (CPU-bound в async endpoint)
- Интеграция с FastAPI: `async def` endpoint, `Depends`, async SQLAlchemy
- Backpressure и rate limiting

