# test_final_state.py

import os
import json
import subprocess
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
HEADERS = {"X-API-Token": "token_ds_7788"}

def test_end_to_end_feature_engineering_flow():
    """
    Executes the end-to-end multi-protocol flow to verify the service behavior.
    """
    # 1. Verify unauthorized access is blocked
    try:
        resp_unauth = requests.get(f"{BASE_URL}/fetch_cleaned", timeout=5)
        assert resp_unauth.status_code in (401, 403), (
            f"Expected 401 or 403 for unauthorized access, got {resp_unauth.status_code}"
        )
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {BASE_URL}: {e}")

    # 2. Trigger feature engineering
    resp_engineer = requests.post(f"{BASE_URL}/engineer_features", headers=HEADERS, timeout=30)
    assert resp_engineer.status_code == 200, (
        f"Expected 200 OK from /engineer_features, got {resp_engineer.status_code}. "
        f"Response body: {resp_engineer.text}"
    )
    try:
        data = resp_engineer.json()
        assert data.get("status") == "engineered", (
            f"Expected JSON body {{'status': 'engineered'}}, got {data}"
        )
    except ValueError:
        pytest.fail(f"Response from /engineer_features was not valid JSON: {resp_engineer.text}")

    # 3. Verify the selected features file
    features_file = "/home/user/selected_features.json"
    assert os.path.exists(features_file), f"File {features_file} does not exist."

    with open(features_file, "r") as f:
        try:
            features = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {features_file} is not valid JSON.")

    assert isinstance(features, list), f"Expected a JSON array in {features_file}, got {type(features)}"
    assert len(features) == 5, f"Expected exactly 5 features in {features_file}, got {len(features)}: {features}"

    # 4. Verify Redis caching directly
    try:
        redis_out = subprocess.check_output(
            ["redis-cli", "-h", "127.0.0.1", "-p", "6379", "GET", "dataset:cleaned"],
            text=True
        ).strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to execute redis-cli GET dataset:cleaned: {e}")

    assert redis_out and redis_out != "(nil)", "Redis key 'dataset:cleaned' is empty or does not exist."

    try:
        redis_data = json.loads(redis_out)
    except json.JSONDecodeError:
        pytest.fail("Redis key 'dataset:cleaned' does not contain valid JSON.")

    assert isinstance(redis_data, list), "Expected Redis 'dataset:cleaned' to contain a JSON array (list of dicts)."

    # 5. Verify the fetch_cleaned endpoint matches Redis
    resp_fetch = requests.get(f"{BASE_URL}/fetch_cleaned", headers=HEADERS, timeout=5)
    assert resp_fetch.status_code == 200, (
        f"Expected 200 OK from /fetch_cleaned, got {resp_fetch.status_code}. "
        f"Response body: {resp_fetch.text}"
    )

    try:
        fetch_data = resp_fetch.json()
    except ValueError:
        pytest.fail(f"Response from /fetch_cleaned was not valid JSON: {resp_fetch.text}")

    assert fetch_data == redis_data, "Data returned from /fetch_cleaned does not match the data cached in Redis."