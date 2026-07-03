# test_final_state.py

import os
import hashlib
import requests
import pytest
import time

def normalize_equation(eq_text):
    # Remove all whitespace characters
    eq_text = "".join(eq_text.split())
    # Convert full-width digits to ASCII
    for i in range(10):
        eq_text = eq_text.replace(chr(0xFF10 + i), str(i))
    # Convert multiplication sign
    eq_text = eq_text.replace("×", "*")
    return eq_text

def get_expected_data():
    csv_path = "/home/user/data/equations.csv"
    assert os.path.isfile(csv_path), f"Missing {csv_path}"

    unique_eqs = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")

    # Skip header
    for line in lines[1:]:
        if not line.strip():
            continue
        # Format is id,equation_text
        parts = line.split(",", 1)
        if len(parts) == 2:
            eq_text = parts[1]
            norm = normalize_equation(eq_text)
            h = hashlib.sha256(norm.encode("utf-8")).hexdigest()
            if h not in unique_eqs:
                unique_eqs[h] = norm

    return unique_eqs

def test_process_math_script_exists():
    script_path = "/home/user/process_math.sh"
    assert os.path.isfile(script_path), f"Missing {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_processed_file_content():
    tsv_path = "/home/user/processed/unique_equations.tsv"
    assert os.path.isfile(tsv_path), f"Missing {tsv_path}"

    expected = get_expected_data()

    with open(tsv_path, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")

    actual = {}
    for line in lines:
        if not line.strip():
            continue
        parts = line.split("\t")
        assert len(parts) == 2, f"Invalid format in TSV line: {line}"
        actual[parts[0]] = parts[1]

    assert actual == expected, "The processed unique equations do not match the expected deduplicated output."

def test_http_server_responses():
    expected = get_expected_data()
    assert len(expected) > 0, "No expected data found to test HTTP server."

    # Wait briefly for server to be up if needed
    time.sleep(1)

    # Test existing hashes
    for h, eq in expected.items():
        url = f"http://127.0.0.1:8080/equation?hash={h}"
        try:
            resp = requests.get(url, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to HTTP server at {url}: {e}")

        assert resp.status_code == 200, f"Expected HTTP 200 for hash {h}, got {resp.status_code}"
        assert resp.text.strip() == eq, f"Expected body '{eq}' for hash {h}, got '{resp.text}'"

    # Test non-existent hash
    fake_hash = "0" * 64
    url = f"http://127.0.0.1:8080/equation?hash={fake_hash}"
    try:
        resp = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server at {url}: {e}")

    assert resp.status_code == 404, f"Expected HTTP 404 for non-existent hash, got {resp.status_code}"

def test_bashttpd_fixed():
    file_path = "/app/bashttpd-0.1/bashttpd"
    assert os.path.isfile(file_path), f"File missing: {file_path}"
    with open(file_path, "r") as f:
        content = f.read()

    # Check that the perturbation was removed or fixed
    assert "REQUEST_URI=$(echo \"$RAW_URI\" | tr -dc 'a-zA-Z0-9/')" not in content, "bashttpd perturbation was not fixed."