import os
import shutil
import pytest
from fastapi.testclient import TestClient
from app import app, data_folder


client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Create a test repo directory
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    yield

    # Teardown: Remove the test repo directory
    if os.path.exists(data_folder):
        shutil.rmtree(data_folder)


def test_list_data_empty():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == []


def test_set_and_get_data():
    key = "test_key"
    value = "test_value"

    # Set data
    response = client.put(f"/{key}", data=value)
    assert response.status_code == 200

    # Get data
    response = client.get(f"/{key}")
    assert response.status_code == 200
    assert response.content.decode("utf-8") == value


def test_delete_data():
    key = "test_key"
    value = "test_value"

    # Set data
    client.put(f"/{key}", data=value)

    # Delete data
    response = client.delete(f"/{key}")
    assert response.status_code == 200

    # Ensure data is deleted
    response = client.get(f"/{key}")
    assert response.status_code == 404


def test_list_data():
    keys_values = {"key1": "value1", "key2": "value2", "key3": "value3"}

    # Set data for multiple keys
    for key, value in keys_values.items():
        client.put(f"/{key}", data=value)

    # List data
    response = client.get("/")
    assert response.status_code == 200
    assert set(response.json()) == set(keys_values.keys())


def test_invalid_key():
    invalid_key = "invalid/key"
    response = client.get(f"/{invalid_key}")
    assert response.status_code == 404
