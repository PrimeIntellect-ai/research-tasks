# test_final_state.py

import os
import csv
import pytest
import requests
import time

def test_extracted_csv_exists_and_correct():
    """Test that the CSV file was extracted and contains the correct data."""
    csv_path = "/home/user/extracted_data.csv"
    assert os.path.isfile(csv_path), f"Extracted CSV not found at {csv_path}"

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader if any(field.strip() for field in row)]

    assert len(rows) >= 4, "CSV should contain at least 4 rows of data"

    # Flatten and clean all cells to do a loose check for the expected numbers
    text_content = " ".join(" ".join(row) for row in rows).replace(",", " ").split()

    expected_values = ["0.0", "100.00", "1.0", "60.65", "2.0", "36.79", "3.0", "22.31"]

    # Check if all expected values are somewhere in the parsed text
    # (OCR might have slight formatting differences, so we check for presence)
    for val in expected_values:
        # Allow slight OCR errors like 100.0 instead of 100.00
        val_float = float(val)
        found = False
        for token in text_content:
            try:
                if abs(float(token) - val_float) < 0.1:
                    found = True
                    break
            except ValueError:
                continue
        assert found, f"Expected value {val} not found in the extracted CSV data"

def test_web_service_auth():
    """Test that the web service enforces authorization."""
    url = "http://localhost:8080/predict"
    payload = {"time": 5.0}

    try:
        r_no_auth = requests.post(url, json=payload, timeout=5)
        assert r_no_auth.status_code in [401, 403], f"Service did not enforce auth, got status code {r_no_auth.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the web service at localhost:8080. Is it running?")

def test_web_service_prediction():
    """Test that the web service returns a valid prediction with correct auth."""
    url = "http://localhost:8080/predict"
    payload = {"time": 5.0}
    headers = {"Authorization": "Bearer chem-sim-2024"}

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        assert r.status_code == 200, f"Expected status code 200, got {r.status_code}. Response: {r.text}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the web service at localhost:8080. Is it running?")

    try:
        data = r.json()
    except ValueError:
        pytest.fail(f"Response was not valid JSON: {r.text}")

    assert "expected_concentration" in data, "Response JSON missing 'expected_concentration' key"

    val = data["expected_concentration"]
    assert isinstance(val, (int, float)), "Expected concentration must be a number"
    assert 7.0 < val < 9.5, f"Concentration out of bounds: {val}. Expected between 7.0 and 9.5"