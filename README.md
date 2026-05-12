# Python Concurrency Practice

Hands-on experiments comparing Python's three concurrency models — threading, multiprocessing, asyncio — under realistic loads. Each topic is a separate folder with runnable snippets, measured timing results, and a focused README explaining what was learned.

## Why this repo exists

Concurrency in Python is famously confusing because the same code behaves differently depending on the workload (CPU vs I/O) and Python version (3.10+ changed GIL behavior, 3.13+ introduced free-threaded build). This repo is a personal reference built by running each model on identical tasks and recording the actual numbers — not memorized theory.

## Stack

- Python 3.14.4 (standard build, GIL enabled)
- stdlib: `threading`, `multiprocessing`, `asyncio`, `queue`
- third-party (for HTTP benchmark only): `requests`, `aiohttp`

## Structure

01-threading/ — threading.Thread, Lock, race conditions, lock granularity
02-multiprocessing/ — Process, Pool, Queue, producer-consumer pattern
03-asyncio/ — coroutines, gather, real HTTP I/O benchmark
04-bridge-async-and-cpu/ — (reserved) run_in_executor, FastAPI + CPU-bound work

Each topic folder has its own README with detailed notes, gotchas, and open topics.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r 03-asyncio/requirements.txt   # only needed for 03-asyncio/03_real_io_speedup.py
```

All other scripts use stdlib only.

## Headline results

Same workload, three models:

| Workload                                                | sequential | threading      | multiprocessing | asyncio       |
| ------------------------------------------------------- | ---------- | -------------- | --------------- | ------------- |
| CPU-bound: count primes in [2, 2M] split into 10 chunks | 5.0 s      | 5.3 s (× 0.95) | 1.3 s (× 3.87)  | —             |
| I/O-bound: 10 HTTP requests to httpbin.org/delay/1      | 31.8 s     | 5.1 s (× 6.2)  | —               | 3.2 s (× 9.8) |

**One-line summary:** threading is useless for CPU-bound work, comparable to asyncio on small I/O, loses to asyncio at scale. Multiprocessing is the only way to bypass the GIL for CPU work. Asyncio wins on I/O scale (memory + context switches).

## Key takeaways

1. **`counter += 1` is not atomic** — three bytecode ops; race condition possible. Lock is the only guarantee.
2. **GIL behavior is implementation-dependent** — Python 3.10+ skips some thread switches in tight primitive loops; need eval breakers (function calls) inside the loop to reliably reproduce race conditions.
3. **`await` does not switch context automatically** — it yields only when the awaitable is not ready. Synchronous code inside `async def` blocks the whole event loop.
4. **`asyncio.sleep` ≠ `time.sleep`** — first yields to event loop, second blocks the thread and breaks everything.
5. **Lock granularity matters** — too wide kills parallelism, too narrow keeps the race. Cover exactly what must be atomic.
6. **Sentinel pattern** for graceful worker shutdown — put `None` (or any agreed value) in the queue, one per worker.

## Decision matrix

CPU-bound (pure Python): multiprocessing
CPU-bound (numpy/C extension): threading (GIL released in C)
I/O-bound, < 100 ops: threading or asyncio (either works)
I/O-bound, 1000+ ops: asyncio (memory and scheduling win)
mixed CPU + I/O in async: asyncio + run_in_executor(ProcessPool)

## Status

- [x] threading — confident middle-junior
- [x] multiprocessing — confident middle-junior
- [x] asyncio basics — confident middle-junior
- [ ] async advanced — `create_task`, `as_completed`, async locks, cancellation, exception handling in `gather`
- [ ] FastAPI integration — `run_in_executor`, blocking endpoints, async SQLAlchemy
- [ ] Higher-level: Celery / RQ / ARQ patterns

## Notes for future me

- Skills decay fast without practice. Re-run all scripts and skim READMEs every ~2 weeks.
- `04-bridge-async-and-cpu/` is reserved for the next round — bridging async event loop to CPU-bound work via `run_in_executor` and demonstrating the same in a FastAPI endpoint that doesn't freeze under load.
- If race conditions stop reproducing in `01-threading/01-race-condition-without-lock.py`, check Python version — GIL behavior changes between versions. Adjust eval breaker (`one()` function call) or use `sys.setswitchinterval(microseconds)`.

- `04-bridge-async-and-cpu/` is reserved for the next round — bridging async event loop to CPU-bound work via `run_in_executor` and demonstrating the same in a FastAPI endpoint that doesn't freeze under load.
- If race conditions stop reproducing in `01-threading/01-race-condition-without-lock.py`, check Python version — GIL behavior changes between versions. Adjust eval breaker (`one()` function call) or use `sys.setswitchinterval(microseconds)`.
