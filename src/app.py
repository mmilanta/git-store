import os
from fastapi import FastAPI, HTTPException, Request, Path
from typing import Annotated
import asyncio
import logging

import git_commands

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


data_folder = os.environ["LOCAL_REPO_FOLDER"]
KeyType = Annotated[str, Path(title="key", pattern="^[^/\0]+$")]


PUSH_DUE: bool = False


async def push_loop():
    global PUSH_DUE
    while True:
        await asyncio.sleep(os.environ["PUSH_EVERY_N_SECONDS"])
        if PUSH_DUE:
            git_commands.push()
            PUSH_DUE = False
        else:
            logger.info("skipping PUSH")

asyncio.create_task(push_loop())

app = FastAPI()


@app.get("/{key}", status_code=200)
async def get_data(key: KeyType) -> bytes:
    check_valid_path(key)
    with open(os.path.join(data_folder, key), "r", encoding="utf-8") as f:
        data = f.read()
    return data.encode("utf-8")


@app.put("/{key}", status_code=200)
async def set_data(key: KeyType, request: Request) -> None:
    path = os.path.join(data_folder, key)
    is_new_file = not os.path.isfile(path)
    with open(path, "w+") as f:
        bystr = await request.body()
        f.write(bystr.decode("utf-8"))

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
