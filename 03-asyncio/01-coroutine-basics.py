import asyncio


async def hello(name):
    print(f"Hello, {name}")


async def main():
    await hello("World")


async def get_value():
    return 42


if __name__ == "__main__":
    print("=== Experiment 1 ===")
    result = hello("world")
    print(result)
    print("=== Experiment 2 ===")
    asyncio.run(hello("World"))
    print("=== Experiment 3 ===")
    asyncio.run(main())
    print("=== Experiment 4 ===")
    value = asyncio.run(get_value())
    print(value)
