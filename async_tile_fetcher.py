import asyncio


def exponential_backoff(f, n=5, err=Exception):
    async def modified(*args, **kwargs):
        for i in range(n):
            try:
                return await f(*args, **kwargs)
            except err:
                if i < n - 1:
                    await asyncio.sleep(2 ** i)
                else:
                    raise err

    return modified


@exponential_backoff
async def fetch(session, url, destination):
    if destination.is_file():
        return destination.read_bytes()
    async with session.get(url) as response:
        response.raise_for_status()
        file_bytes = await response.read()
        destination.write_bytes(file_bytes)
        return file_bytes


async def gather_progress(awaitables):
    """
    Gather awaitables, printing the completion ratio to stdout
    """
    done = []

    async def print_percent(awaitable, done):
        res = await awaitable
        done.append(res)
        msg = "{:.1f}%".format(100 * len(done) / len(awaitables))
        print(msg, end='\r')
        return res

    total = await asyncio.gather(*[
        print_percent(a, done)
        for i, a in enumerate(awaitables)
    ])
    print()  # Print a new line after the percentages
    return total
