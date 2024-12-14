pip install -r requirements.txt
export PYTHONPATH=src
export $(grep -v '^#' .env | xargs)
uvicorn src.app:app --host 0.0.0.0 --port 5000 --reload --log-level=debug