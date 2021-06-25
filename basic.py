import asyncio

from loguru import logger
import typer

app = typer.Typer()


async def a():
    name = "a"
    logger.debug(f"start {name}")
    await asyncio.sleep(1)
    logger.debug(f"end {name}")
    return name


async def b():
    name = "b"
    logger.debug(f"start {name}")
    await asyncio.sleep(1)
    logger.debug(f"end {name}")
    return name


@app.command()
def sequential():
    asyncio.run(a_b_sequential())


@app.command()
def parallel():
    asyncio.run(a_b_parallel())


async def a_b_sequential():
    name = "a_b_sequential"

    logger.debug(f"start {name}")
    ret_a = await a()
    ret_b = await b()
    logger.debug(f"end {name}")
    logger.debug(f"{ret_a=},{ret_b=}")


async def a_b_parallel():
    name = "a_b_parallel"

    logger.debug(f"start {name}")
    tasks = list()
    tasks.append(asyncio.create_task(a(), name="a"))
    tasks.append(asyncio.create_task(b(), name="b"))
    done, doing = await asyncio.wait(tasks)
    for item in done:
        # logger.debug(dir(item))
        if item.get_name() == "a":
            ret_a = item.result()
        else:
            ret_b = item.result()

    logger.debug(f"end {name}")
    logger.debug(f"{ret_a=},{ret_b=}")


if __name__ == "__main__":
    app()
