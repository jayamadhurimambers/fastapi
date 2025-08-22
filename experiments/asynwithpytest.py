import asyncio

async def task(name, delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)   # simulate work
    print(f"Task {name} finished after {delay} seconds")

async def main():
    # Run tasks concurrently
    await asyncio.gather(
        task("madhuri", 2),
        task("sharavan", 1),
        task("manvik", 3)
    )

if __name__ == "__main__":
    asyncio.run(main())
