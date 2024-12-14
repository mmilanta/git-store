IMAGE = git-store
export PYTHONPATH := src\


.PHONY: compile
compile:
	pip-compile -o requirements.txt --extra dev pyproject.toml

.PHONY: build
build:
	docker build . -t $(IMAGE)

.PHONY: tests
tests:
	docker run -it --env-file ci.env -e SKIP_REMOTE_CONNECTION=true $(IMAGE) pytest tests.py -v -ss --log-cli-level=INFO


.PHONY: run-local
run:
	docker run -it --env-file .env -p 5000:5000 $(IMAGE)

.PHONY: run-venv
run-venv:
	sh ./run_on_venv.sh