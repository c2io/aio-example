import asyncio
import time
from typing import List

from loguru import logger
import typer
import aiohttp
import aiofiles
import requests

app = typer.Typer()
logger.add("cost.log", level="INFO")


@app.command()
def adownload(count: int):
    start_time = time.time()
    asyncio.run(aio_download(count))
    end_time = time.time()
    logger.info(f"{count=},{end_time-start_time=}")


@app.command()
def adownload2(count: int):
    start_time = time.time()
    asyncio.run(aio_download2(count))
    end_time = time.time()
    logger.info(f"{count=},{end_time-start_time=}")


download_files = ["http://127.0.0.1:8000/a.txt"] * 3000
log_count = 100


@app.command()
def download(count: int = 1):
    start_time = time.time()

    with requests.Session() as session:
        for index, item in enumerate(download_files):
            # if index % log_count == 0:
            #     logger.debug(f"{index=}")
            content = session.get(item).content
            # with open(f"data/{index}.txt", "wb") as file:
            #     file.write(content)

    end_time = time.time()
    logger.info(f"{count=},{end_time-start_time=}")


async def write(filename: str, content: bytes):
    async with aiofiles.open(filename, "wb") as file:
        await file.write(content)


async def down(session: aiohttp.ClientSession, url: str):
    response = await session.get(url)
    return await response.content.read()


async def down_and_write(session: aiohttp.ClientSession, url: str, filename: str):
    response = await session.get(url)
    content = await response.content.read()
    # await write(filename, content)


async def down_and_write2(urls: List[str]):
    async with aiohttp.ClientSession() as session:
        for url in urls:
            response = await session.get(url)
            content = await response.content.read()  #


async def aio_download2(count: int):
    tasks = list()

    for i in range(count):
        piece_count = len(download_files) // count
        start_index, end_index = i * piece_count, (i + 1) * piece_count
        files = list()
        for file in download_files[start_index:end_index]:
            files.append(file)
        tasks.append(asyncio.create_task(down_and_write2(files)))

    await asyncio.wait(tasks)


async def aio_download(count: int):

    tasks = list()
    async with aiohttp.ClientSession() as session:
        for index, item in enumerate(download_files):
            tasks.append(
                asyncio.create_task(down_and_write(session, item, f"data/{index}.txt"))
            )

            if len(tasks) >= count:
                done, _ = await asyncio.wait(tasks)
                for done_item in done:
                    pass
                tasks.clear()
        else:
            if tasks:
                done, _ = await asyncio.wait(tasks)


if __name__ == "__main__":
    app()
