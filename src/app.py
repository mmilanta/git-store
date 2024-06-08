import os
from fastapi import FastAPI, HTTPException, Request, Path, BackgroundTasks
from typing import Annotated

import git_commands

app = FastAPI()

data_folder = os.environ["LOCAL_REPO_FOLDER"]
KeyType = Annotated[str, Path(title="key", pattern="^[^/\0]+$")]


@app.get("/{key}", status_code=200)
async def get_data(key: str) -> bytes:
    check_valid_path(key)
    with open(os.path.join(data_folder, key), "r", encoding="utf-8") as f:
        data = f.read()
    return data.encode("utf-8")


@app.put("/{key}", status_code=200)
async def set_data(key: KeyType, request: Request, background_tasks: BackgroundTasks) -> None:
    path = os.path.join(data_folder, key)
    is_new_file = not os.path.isfile(path)
    with open(path, "w+") as f:
        bystr = await request.body()
        f.write(bystr.decode("utf-8"))

    background_tasks.add_task(
        git_commands.commit_and_push,
        file_path=key,
        commit_message=("new" if is_new_file else "edit") + f": {key}",
    )


@app.delete("/{key}", status_code=200)
async def delete_data(key: KeyType, background_tasks: BackgroundTasks) -> None:
    check_valid_path(key)
    os.remove(os.path.join(data_folder, key))

    background_tasks.add_task(
        git_commands.commit_and_push,
        file_path=None,
        commit_message=f"deleted: {key}"
    )


@app.get("/", status_code=200)
async def list_data() -> list[str]:
    return [entry for entry in os.listdir(data_folder)]


def check_valid_path(key: KeyType):
    if not os.path.isfile(os.path.join(data_folder, key)):
        raise HTTPException(status_code=404, detail="Key not found")
