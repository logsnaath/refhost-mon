#!/usr/bin/python3
##
## Author: Logu R<logu.rangasamy@suse.com>
## 

import asyncio

async def say_hello(delay, name):
    await asyncio.sleep(delay)
    print(f"Hello, {name}! (after {delay} seconds)")

async def main():
    # Create a list of tasks
    tasks=[]
    for i in range(5):
        tasks.append (say_hello(i, f"Person{i}"))

    # Run tasks concurrently using asyncio.gather
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
