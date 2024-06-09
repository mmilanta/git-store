import os
from fastapi import FastAPI, HTTPException, Request, Path, Response
from typing import Annotated
import asyncio
import logging
import aiofiles

import git_commands

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


data_folder = os.environ["LOCAL_REPO_FOLDER"]
KeyType = Annotated[str, Path(title="key", pattern="^[^/\0]+$")]


PUSH_DUE: bool = False


async def push_loop():
    global PUSH_DUE
    while True:
        await asyncio.sleep(int(os.environ["PUSH_EVERY_N_SECONDS"]))
        if PUSH_DUE:
            git_commands.push()
            PUSH_DUE = False
        else:
            logger.info("skipping PUSH")

asyncio.create_task(push_loop())

app = FastAPI()


@app.get("/{key}")
async def get_data(key: KeyType) -> bytes:
    check_valid_path(key)
    async with aiofiles.open(os.path.join(data_folder, key), "rb") as f:
        data = await f.read()
    return Response(content=data, status_code=200)


@app.put("/{key}", status_code=200)
async def set_data(key: KeyType, request: Request) -> None:
    path = os.path.join(data_folder, key)
    is_new_file = not os.path.isfile(path)
    async with aiofiles.open(path, "wb+") as f:
        bystr = await request.body()
        await f.write(bystr)

    git_commands.commit(
        file_path=key,
        commit_message=("new" if is_new_file else "edit") + f": {key}",
    )
    global PUSH_DUE
    PUSH_DUE = True


@app.delete("/{key}", status_code=200)
async def delete_data(key: KeyType) -> None:
    check_valid_path(key)
    os.remove(os.path.join(data_folder, key))

    git_commands.commit(
        file_path=None,
        commit_message=f"deleted: {key}"
    )
    global PUSH_DUE
    PUSH_DUE = True


@app.get("/", status_code=200)
async def list_data() -> list[str]:
    return [entry for entry in os.listdir(data_folder)]


def check_valid_path(key: KeyType):
    if not os.path.isfile(os.path.join(data_folder, key)):
        raise HTTPException(status_code=404, detail="Key not found")
