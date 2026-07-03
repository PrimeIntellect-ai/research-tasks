# test_final_state.py

import os
import requests
import pytest

RAW_DATA = "/home/user/data/raw_data.csv"
CLEAN_DATA = "/home/user/data/clean_data.csv"
URL_BASE = "http://localhost:8888/payload/"

def is_clean(f1, f2, f3):
    return (3.0 * f1) - (2.0 * f2) + f3 <= 100.0

@pytest.fixture(scope="module")
def sample_data():
    clean_samples = []
    dirty_samples = []

    if not os.path.exists(RAW_DATA):
        pytest.fail(f"Raw data file {RAW_DATA} is missing.")

    with open(RAW_DATA, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 5:
                row_id = parts[0]
                try:
                    f1, f2, f3 = float(parts[1]), float(parts[2]), float(parts[3])
                except ValueError:
                    continue

                payload = parts[4]

                if is_clean(f1, f2, f3):
                    if len(clean_samples) < 5:
                        clean_samples.append((row_id, payload))
                else:
                    if len(dirty_samples) < 5:
                        dirty_samples.append((row_id, payload))

            if len(clean_samples) >= 5 and len(dirty_samples) >= 5:
                break

    return clean_samples, dirty_samples

def test_clean_data_file_exists():
    assert os.path.exists(CLEAN_DATA), f"Missing cleaned data file at {CLEAN_DATA}"
    assert os.path.isfile(CLEAN_DATA), f"{CLEAN_DATA} is not a file"
    assert os.path.getsize(CLEAN_DATA) > 0, f"{CLEAN_DATA} is empty"

def test_api_clean_records(sample_data):
    clean_samples, _ = sample_data
    assert len(clean_samples) > 0, "No clean samples found in raw_data.csv"

    for row_id, expected_payload in clean_samples:
        try:
            resp = requests.get(f"{URL_BASE}{row_id}", timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to API for clean ID {row_id}: {e}")

        assert resp.status_code == 200, f"Expected 200 OK for clean ID {row_id}, got {resp.status_code}. Response: {resp.text}"
        assert expected_payload in resp.text, f"Expected payload '{expected_payload}' for ID {row_id}, but got: {resp.text}"

def test_api_dirty_records(sample_data):
    _, dirty_samples = sample_data
    assert len(dirty_samples) > 0, "No dirty samples found in raw_data.csv"

    for row_id, _ in dirty_samples:
        try:
            resp = requests.get(f"{URL_BASE}{row_id}", timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to API for dirty ID {row_id}: {e}")

        assert resp.status_code == 404, f"Expected 404 Not Found for dirty ID {row_id}, got {resp.status_code}. Response: {resp.text}"

def test_api_nonexistent_record():
    fake_id = "999999999"
    try:
        resp = requests.get(f"{URL_BASE}{fake_id}", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API for non-existent ID {fake_id}: {e}")

    assert resp.status_code == 404, f"Expected 404 Not Found for non-existent ID {fake_id}, got {resp.status_code}. Response: {resp.text}"