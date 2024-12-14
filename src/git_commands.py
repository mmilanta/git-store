from git import Repo
import os
import logging
import shutil


logger = logging.getLogger(__name__)

if os.path.isdir(os.environ["LOCAL_REPO_FOLDER"]):
    shutil.rmtree(os.environ["LOCAL_REPO_FOLDER"])


if os.environ.get("SKIP_REMOTE_CONNECTION", False):
    repo = Repo.init(os.environ["LOCAL_REPO_FOLDER"])
    logger.info("init repo")
else:
    logger.info("cloning repo")
    repo = Repo.clone_from(os.environ["REPO_URL"], os.environ["LOCAL_REPO_FOLDER"])

logger.info("setting username and email")
repo.config_writer().set_value("user", "name", os.environ["USER_NAME"]).release()
repo.config_writer().set_value("user", "email", os.environ["USER_EMAIL"]).release()


def commit(file_path: str | None, commit_message: str):
    if file_path is not None:
        repo.index.add([file_path])
    else:
        repo.git.add(u=True)
    logger.info(f"committing {commit_message}")
    repo.index.commit(commit_message)


def push():
    try:
        origin = repo.remote(name='origin')
    except ValueError:
        logger.info("Skipping due to missing remote origin")
        return
    logger.info("pushing to remote")
    origin.push()
