import asyncio


async def fastest_sort_ever_made(container: list[int]):
    async def worker(item: int):
        await asyncio.sleep(item)
        return item

    tasks = [asyncio.create_task(worker(item)) for item in container]

    results = []
    async for task in asyncio.as_completed(tasks):
        results.append(task.result())

    return results


async def fastest_find_closest_leaf_ever_made(node):
    """
    Also, this is (surely) the first time breadth-first search has been done recursively.
    """

    if node.is_leaf():
        return node

    await asyncio.sleep(1)

    tasks = [
        asyncio.create_task(fastest_find_closest_leaf_ever_made(child))
        for child in node.children
    ]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for task in pending:
        task.cancel()

    return next(iter(done)).result()
