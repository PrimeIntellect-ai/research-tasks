# test_final_state.py
import os
import csv
import time
import pytest
import requests
import subprocess

def test_long_translations_csv():
    path = "/home/user/data/processed/long_translations.csv"
    assert os.path.isfile(path), f"Missing {path}"

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames, "CSV is empty or missing headers"
        headers = [h.strip() for h in reader.fieldnames]
        assert "key" in headers, "Missing 'key' column"
        assert "locale" in headers, "Missing 'locale' column"
        assert "translation" in headers, "Missing 'translation' column"

        rows = list(reader)
        assert len(rows) > 0, "No data rows in long_translations.csv"

        # Check imputation logic
        for row in rows:
            if row["translation"].startswith("[UNTRANSLATED] "):
                assert len(row["translation"]) > len("[UNTRANSLATED] "), "Imputed string is empty after prefix"

def test_qa_sample_csv():
    long_path = "/home/user/data/processed/long_translations.csv"
    qa_path = "/home/user/data/processed/qa_sample.csv"

    assert os.path.isfile(qa_path), f"Missing {qa_path}"

    with open(long_path, "r", encoding="utf-8") as f:
        long_keys = set(row["key"] for row in csv.DictReader(f))

    with open(qa_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        qa_rows = list(reader)
        qa_keys = set(row["key"] for row in qa_rows)

    assert len(qa_keys) > 0, "qa_sample.csv has no keys"

    # Check 10% sampling
    expected_sample_size = int(len(long_keys) * 0.10)
    # allow a small margin due to rounding
    assert abs(len(qa_keys) - expected_sample_size) <= 1, f"Expected ~{expected_sample_size} keys in QA sample, found {len(qa_keys)}"

def test_http_server_endpoint():
    # Attempt to connect to the server, retrying a few times in case it's slow to start
    url = "http://127.0.0.1:8080/api/v1/strings?locale=fr_FR"
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(1)
    else:
        pytest.fail("Could not connect to HTTP server at 127.0.0.1:8080 or it did not return 200 OK")

    data = response.json()
    assert isinstance(data, dict), "Response should be a JSON object"
    assert len(data) > 0, "Returned JSON object is empty"

    # Check that keys are mapped to strings
    for k, v in data.items():
        assert isinstance(k, str), "Keys must be strings"
        assert isinstance(v, str), "Values must be strings"

    # Check if there are any imputed strings to verify the logic
    imputed_found = any(v.startswith("[UNTRANSLATED] ") for v in data.values())
    # We can't strictly assert imputed_found is True without knowing the data, but it's highly likely