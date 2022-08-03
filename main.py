#!/usr/bin/env python3
import asyncio
import logging
import os
import pathlib
from typing import AsyncIterable

from aiohttp import ClientConnectorError
from yapapi import Golem, Task, WorkContext, NoPaymentAccountError
from yapapi.log import enable_default_logger
from yapapi.payload import vm

log = logging.getLogger(__name__)
os.environ["YAGNA_APPKEY"] = "55359a3e7afb4525be26fff47accc41f"


async def worker(context: WorkContext, tasks: AsyncIterable[Task]):
    async for task in tasks:
        script_dir = pathlib.Path(__file__).resolve().parent
        script = context.new_script()
        await script.upload_file(str(script_dir / "task.py"), "/golem/resource/task.py")
        future_result = script.run("python3", "/golem/resource/task.py")

        yield script

        task.accept_result(result=await future_result)


async def main():
    package = await vm.repo(
        image_hash="d646d7b93083d817846c2ae5c62c72ca0507782385a2e29291a3d376",
    )

    tasks = [Task(data=None)]

    try:
        async with Golem(budget=1.0, subnet_tag="devnet-beta") as golem:
            async for completed in golem.execute_tasks(worker, tasks, payload=package):
                print(completed.result.stdout)
    except NoPaymentAccountError:
        raise
    except ClientConnectorError as ex:
        log.error(f"Yagna client is not running!\nPlease run \"yagna service run\" or consult the docs\nError: {ex}")


if __name__ == "__main__":
    enable_default_logger(log_file="hello.log")

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)