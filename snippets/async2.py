#!/usr/bin/python3
##
## Author: Logu R<logu.rangasamy@suse.com>
##

import asyncio

async def say_hello(delay, name):
    await asyncio.sleep(delay)
    print(f"Hello, {name}! (after {delay} seconds)")

async def main():
    # Schedule multiple coroutines concurrently
    task1 = asyncio.create_task(say_hello(2, "Alice"))
    task2 = asyncio.create_task(say_hello(1, "Bob"))

    # Wait for all tasks to complete
    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    asyncio.run(main())

