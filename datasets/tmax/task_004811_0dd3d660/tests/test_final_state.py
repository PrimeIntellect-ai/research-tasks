# test_final_state.py

import os
import requests
import pytest

def test_clean_datasets_files():
    clean_dir = "/home/user/clean_datasets"
    assert os.path.isdir(clean_dir), f"Directory {clean_dir} does not exist"

    valid1_path = os.path.join(clean_dir, "valid1.txt")
    valid2_path = os.path.join(clean_dir, "valid2.txt")

    assert os.path.isfile(valid1_path), f"File {valid1_path} does not exist"
    assert os.path.isfile(valid2_path), f"File {valid2_path} does not exist"

    with open(valid1_path, "r") as f:
        assert f.read() == "BIOSEQ_v2\tATGC", f"Content of {valid1_path} is incorrect"

    with open(valid2_path, "r") as f:
        assert f.read() == "BIOSEQ_v2\tCGTA", f"Content of {valid2_path} is incorrect"

def test_http_list():
    url = "http://127.0.0.1:9090/list"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON: {response.text}")

    assert isinstance(data, list), "Response JSON should be a list"
    assert "valid1.txt" in data, "valid1.txt not found in /list response"
    assert "valid2.txt" in data, "valid2.txt not found in /list response"
    assert len(data) == 2, f"Expected exactly 2 files in list, got {len(data)}"

def test_http_data_valid1():
    url = "http://127.0.0.1:9090/data/valid1.txt"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.text == "BIOSEQ_v2\tATGC", f"Content for valid1.txt is incorrect: {response.text}"

def test_http_data_valid2():
    url = "http://127.0.0.1:9090/data/valid2.txt"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.text == "BIOSEQ_v2\tCGTA", f"Content for valid2.txt is incorrect: {response.text}"