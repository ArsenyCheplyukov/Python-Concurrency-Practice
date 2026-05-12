import asyncio
import queue
import threading
from time import perf_counter

import aiohttp
import requests

URLS = ["https://httpbin.org/delay/1"] * 10


def fetch_sync(url):
    response = requests.get(url)
    return len(response.content)


def fetch_thread(url, q):
    response = requests.get(url)
    q.put(len(response.content))


async def fetch_async(session, url):
    async with session.get(url) as response:
        content = await response.read()
        return len(content)


def run_sync():
    return [fetch_sync(url) for url in URLS]


async def run_async():
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*[fetch_async(session, url) for url in URLS])


def run_threads():
    threads = []
    q = queue.Queue()
    for url in URLS:
        thread = threading.Thread(target=fetch_thread, args=(url, q))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return [q.get() for _ in range(len(URLS))]


if __name__ == "__main__":
    print("=== Sync (requests) ===")
    t0 = perf_counter()
    sync_results = run_sync()
    print(f"Time: {perf_counter() - t0:.2f}s, got {len(sync_results)} responses")

    print("=== Async (aiohttp) ===")
    t0 = perf_counter()
    async_results = asyncio.run(run_async())
    print(f"Time: {perf_counter() - t0:.2f}s, got {len(async_results)} responses")

    print("=== Threads (requests) ===")
    t0 = perf_counter()
    thread_results = run_threads()
    print(f"Time: {perf_counter() - t0:.2f}s, got {len(thread_results)} responses")
