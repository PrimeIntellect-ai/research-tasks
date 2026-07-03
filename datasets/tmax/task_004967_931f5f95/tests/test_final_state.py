# test_final_state.py

import os
import glob
import requests
import pytest

def compute_expected_sum():
    total_sum = 0
    csv_files = glob.glob("/home/user/data/part_*.csv")
    for file_path in csv_files:
        with open(file_path, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:  # skip header
                parts = line.strip().split(",")
                if len(parts) >= 4:
                    try:
                        age = int(parts[2])
                        score = int(parts[3])
                        if age >= 18 and score >= 50:
                            total_sum += score
                    except ValueError:
                        continue
    return total_sum

def test_filter_valid_script_fixed():
    file_path = "/app/bash-csv-toolkit-1.2/filter_valid.sh"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    assert 'MIN_SCOR=' not in content, "The typo 'MIN_SCOR=' is still present in the script."
    assert 'MIN_SCORE="$MIN_SCORE"' in content or 'MIN_SCORE=' in content, "The script does not properly assign MIN_SCORE."

def test_sum_file_correct():
    expected_sum = compute_expected_sum()
    sum_file_path = "/home/user/sum.txt"
    assert os.path.isfile(sum_file_path), f"File {sum_file_path} does not exist."

    with open(sum_file_path, "r") as f:
        content = f.read().strip()

    assert content == str(expected_sum), f"Expected sum {expected_sum} in {sum_file_path}, but got {content}."

def test_http_server_response():
    expected_sum = compute_expected_sum()
    url = "http://127.0.0.1:8080/"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP status 200, but got {response.status_code}."

    body = response.text.strip()
    assert str(expected_sum) in body, f"Expected the response body to contain '{expected_sum}', but got '{body}'."