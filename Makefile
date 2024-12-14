IMAGE = git-store
export PYTHONPATH := src
include .env


.PHONY: compile
compile:
	pip-compile -o requirements.txt --extra dev pyproject.toml

.PHONY: tests
tests:
	docker build . -t $(IMAGE)
	docker run -it --env-file .env -e SKIP_REMOTE_CONNECTION=true $(IMAGE) pytest tests.py -v -ss --log-cli-level=INFO


.PHONY: run
run:
	docker build . -t $(IMAGE)
	docker run -it --env-file .env -p 5000:5000 $(IMAGE)

.PHONY: run-venv
run-venv:
	sh ./run_on_venv.sh