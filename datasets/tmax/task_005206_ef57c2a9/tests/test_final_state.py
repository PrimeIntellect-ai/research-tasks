# test_final_state.py
import os
import requests
import pytest

def test_ready_file_exists():
    assert os.path.isfile("/home/user/ready.txt"), "The /home/user/ready.txt file was not created. Did the server start successfully?"

def test_api_merged_endpoint_electronics():
    url = "http://127.0.0.1:8000/api/merged"
    params = {
        "category": "Electronics",
        "sort": "sale_id",
        "order": "asc",
        "limit": 1,
        "offset": 1
    }

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert isinstance(data, list), "Expected response to be a JSON list of dictionaries."
    assert len(data) == 1, f"Expected exactly 1 item in the response, got {len(data)}. Data: {data}"

    item = data[0]
    assert str(item.get("sale_id")) == "2", f"Expected sale_id '2', got {item.get('sale_id')}"
    assert str(item.get("product_id")) == "102", f"Expected product_id '102', got {item.get('product_id')}"
    assert str(item.get("category")) == "Electronics", f"Expected category 'Electronics', got {item.get('category')}"
    assert str(item.get("name")) == "Headphones", f"Expected name 'Headphones', got {item.get('name')}"

def test_api_merged_endpoint_kitchen_desc():
    url = "http://127.0.0.1:8000/api/merged"
    params = {
        "sort": "sale_id",
        "order": "desc",
        "limit": 2,
        "offset": 0
    }

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert isinstance(data, list), "Expected response to be a JSON list of dictionaries."
    assert len(data) == 2, f"Expected exactly 2 items in the response, got {len(data)}. Data: {data}"

    # Sort by sale_id desc -> sale_id 4, then 3
    assert str(data[0].get("sale_id")) == "4", f"Expected first item sale_id '4', got {data[0].get('sale_id')}"
    assert str(data[1].get("sale_id")) == "3", f"Expected second item sale_id '3', got {data[1].get('sale_id')}"

def test_bug_fixed_in_engine():
    engine_py = "/app/pylitecsv-1.0.0/pylitecsv/engine.py"
    assert os.path.isfile(engine_py), f"Missing file: {engine_py}"
    with open(engine_py, "r") as f:
        content = f.read()

    # Check that the cross join is no longer just returning all combinations without a condition
    assert "==" in content or "if" in content or "match" in content, "The inner_join method does not seem to have a condition to check for key equality."