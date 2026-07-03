# test_final_state.py

import os
import requests
import pytest

def test_api_running_and_correct():
    url = "http://127.0.0.1:9090/calculate"
    params = {"expr": "10+20*3"}
    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API on 127.0.0.1:9090: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    text = response.text.strip()
    try:
        result = float(text)
    except ValueError:
        pytest.fail(f"API response body could not be parsed as a float: '{text}'")

    assert result == 70.0, f"Expected API to return 70.0 for '10+20*3', but got {result}"

def test_file_organization():
    high_file = "/home/user/configs_high/file1.txt"
    low_file = "/home/user/configs_low/file2.txt"

    assert os.path.isfile(high_file), f"Expected {high_file} to exist (150 > 100)."
    assert os.path.isfile(low_file), f"Expected {low_file} to exist (30 <= 100)."

    # Check that they were moved, not copied
    assert not os.path.exists("/home/user/configs/file1.txt"), "file1.txt should have been moved, but it still exists in /home/user/configs."
    assert not os.path.exists("/home/user/configs/file2.txt"), "file2.txt should have been moved, but it still exists in /home/user/configs."

def test_benchmark_file():
    benchmark_file = "/home/user/benchmark.txt"
    assert os.path.isfile(benchmark_file), f"Expected benchmark file {benchmark_file} does not exist."

    with open(benchmark_file, "r") as f:
        content = f.read().strip()

    try:
        time_val = float(content)
    except ValueError:
        pytest.fail(f"Benchmark file does not contain a valid float: '{content}'")

    assert time_val >= 0.0, f"Benchmark time should be a positive float, got {time_val}"