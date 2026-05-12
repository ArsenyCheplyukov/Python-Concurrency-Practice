import asyncio
from time import perf_counter


async def fetch(name, delay):
    print(f"[{name}] start")
    await asyncio.sleep(delay)
    print(f"[{name}] done after {delay}s")
    return f"result_{name}"


async def run_sequential():
    start_time = perf_counter()
    r1 = await fetch("A", 1)
    r2 = await fetch("B", 1)
    r3 = await fetch("C", 1)
    print(f"Time passed: {perf_counter() - start_time}")
    return [r1, r2, r3]


async def run_gathered():
    start_time = perf_counter()
    results = await asyncio.gather(
        fetch("A", 1),
        fetch("B", 1),
        fetch("C", 1),
    )
    print(f"Time passed: {perf_counter() - start_time}")
    return results


if __name__ == "__main__":
    print("=== Sequential ===")
    print(f"Sequential result is: {asyncio.run(run_sequential())}")
    print("=== Gathered ===")
    print(f"Gathered result is: {asyncio.run(run_gathered())}")
