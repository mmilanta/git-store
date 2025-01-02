# Git Store
A simple key-value store that persists everything on git, allowing to keep track of history.
Disclaimer:
## Setup
### Add it to your app
When using docker composer, you can pull the image from a public registry.
```yaml
  git-store:
    image: ghcr.io/mmilanta/git-store:main
    command: >
      sh -c "uvicorn app:app --host 0.0.0.0 --port 5000"
    ports:
      - "5000:5000"
    env_file:
      - .env-git-store
```
### ENV variables
To run `git-store`, we need a few env variables.
```env
LOCAL_REPO_FOLDER=local_data
PUSH_EVERY_N_SECONDS=5 # how often it synces with remote (if no edits are done, no syncing is happening)
GITHUB_PAT=github_pat_ ... # Github PAT that has access to write to the repo
REPO=my_user/my_repo # Repo to use as store
REPO_URL=https://${GITHUB_PAT}@github.com/${REPO}
USER_NAME=git-store # username that will make commits to the repo
USER_EMAIL=git-store@fake.com # email that will make commits to the repo
```
## Use it
To use it you can make `http` requests at the following endpoints:
* To list all available keys: `curl -X GET --url 'http://127.0.0.1:5000/'`
* To get value from key `key_sample`: `curl -X GET --url 'http://127.0.0.1:5000/key_sample'`
* To set value of key `key_sample` to `Ehi, come va?`: `curl -X PUT --url 'http://127.0.0.1:5000/key_sample' --data 'Ehi, come va?'`
* To delete key `key_sample`: `curl -X DELETE --url 'http://127.0.0.1:5000/key_sample'`
