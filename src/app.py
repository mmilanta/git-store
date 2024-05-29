import os

from fastapi import FastAPI, HTTPException, Request

import git_commands

app = FastAPI()

data_folder = "recipe-data"


@app.get("/{key}")
async def get_data(key: str) -> bytes:
    with open(os.path.join(data_folder, key), "r", encoding="utf-8") as f:
        data = f.read()
    return data.encode("utf-8")


@app.put("/{key}")
async def set_data(key: str, request: Request) -> None:
    path = os.path.join(data_folder, key)
    is_new_file = not os.path.isfile(path)
    with open(path, "w+") as f:
        bystr = await request.body()
        f.write(bystr.decode("utf-8"))
    git_commands.commit_and_push(
        file_path=key,
        commit_message="new" if is_new_file else "edit" + f": {key}",
    )


@app.delete("/{key}")
async def delete_data(key: str) -> None:
    check_valid_path(key)
    os.remove(os.path.join(data_folder, key))
    git_commands.commit_and_push(
        file_path=None, commit_message=f"deleted: {key}"
    )


@app.get("/")
async def list_data() -> list[str]:
    return [entry for entry in os.listdir(data_folder)]


def check_valid_path(key: str):
    if not os.path.isfile(key):
        raise HTTPException(status_code=404, detail="Key not found")
