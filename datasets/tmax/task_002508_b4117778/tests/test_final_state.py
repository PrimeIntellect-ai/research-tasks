# test_final_state.py

import os
import requests
import pytest

def test_final_state():
    data_path = "/home/user/data.csv"
    assert os.path.isfile(data_path), f"Missing original data file: {data_path}"

    with open(data_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1000, f"Expected 1000 rows in {data_path}, found {len(lines)}"

    # Compute the training mean (first 800 rows)
    train_sum = 0.0
    train_count = 0
    for line in lines[:800]:
        parts = line.split(",")
        val = float(parts[1])
        if val != -999.0:
            train_sum += val
            train_count += 1

    train_mean = train_sum / train_count if train_count > 0 else 0.0

    # Compute the expected final test set
    expected_lines = []
    for line in lines[800:]:
        parts = line.split(",")
        id_str = parts[0]
        val = float(parts[1])

        if val == -999.0:
            val = train_mean

        # The C code uses %.2f for output
        val_formatted = f"{val:.2f}"
        val_parsed = float(val_formatted)

        # Outlier scorer logic: score = fabs(val - 50.0) / 20.0
        score = abs(val_parsed - 50.0) / 20.0

        if score <= 0.80:
            expected_lines.append(f"{id_str},{val_formatted}")

    # Fetch from the HTTP server
    url = "http://127.0.0.1:8080/final_test.csv"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text[:200]}"

    actual_content = response.text

    # Compare actual vs expected
    actual_lines = [line.strip() for line in actual_content.strip().split("\n") if line.strip()]

    assert actual_lines == expected_lines, "The downloaded final_test.csv does not match the expected output. Either the mean was computed incorrectly, the imputation failed, or the outlier filtering was incorrect."