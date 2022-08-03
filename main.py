import os
from datetime import timedelta

os.environ["YAGNA_APPKEY"] = "55359a3e7afb4525be26fff47accc41f"
import asyncio
import logging
import pathlib
from typing import AsyncIterable

from aiohttp import ClientConnectorError
from yapapi import Golem, Task, WorkContext, NoPaymentAccountError
from yapapi.log import enable_default_logger
from yapapi.payload import vm

log = logging.getLogger(__name__)


async def worker(context: WorkContext, tasks: AsyncIterable[Task]):
    async for task in tasks:
        script_dir = pathlib.Path(__file__).resolve().parent
        script = context.new_script(timeout=timedelta(minutes=10))
        script.upload_file(str(script_dir / "task.py"), "/golem/output/task.py")
        future_result = script.run("/usr/bin/python3", "/golem/output/task.py", task.data)
        yield script
        task.accept_result(result=await future_result)


async def main():
    package = await vm.repo(
        image_hash="9a3b5d67b0b27746283cb5f287c13eab1beaa12d92a9f536b747c7ae",
    )

    tasks = [Task(data="Łukasz")]

    try:
        async with Golem(budget=1.0, subnet_tag="devnet-beta") as golem:
            async for completed in golem.execute_tasks(worker, tasks, payload=package):
                print(completed.result.stdout)
    except NoPaymentAccountError:
        raise
    except (ConnectionResetError, ClientConnectorError) as ex:
        log.error(f"Yagna client is not running!\nPlease run \"yagna service run\" or consult the docs\nError: {ex}")
        raise


if __name__ == "__main__":
    enable_default_logger(log_file="hello.log")

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)