# test_final_state.py
import os
import json
import pytest
import requests
from collections import defaultdict

RAW_LOGS_PATH = "/home/user/raw_logs.tsv"
TOP_ERRORS_PATH = "/home/user/top_errors.txt"
STRATIFIED_ERRORS_PATH = "/home/user/stratified_errors.tsv"
INSTALLED_SCRIPT_PATH = "/home/user/bin/stratify_errors"
SERVER_URL = "http://127.0.0.1:9090"

def get_expected_data():
    """Derive expected top errors and stratified errors from the raw logs."""
    if not os.path.exists(RAW_LOGS_PATH):
        return [], []

    error_counts = defaultdict(int)
    stratified_lines = []
    stratified_counts = defaultdict(int)

    with open(RAW_LOGS_PATH, "r") as f:
        for line in f:
            parts = line.strip('\n').split('\t')
            if len(parts) < 5:
                continue
            endpoint = parts[3]
            try:
                status = int(parts[4])
            except ValueError:
                continue

            if status >= 400:
                error_counts[endpoint] += 1
                if stratified_counts[endpoint] < 2:
                    stratified_lines.append(line.strip('\n'))
                    stratified_counts[endpoint] += 1

    # Sort by frequency descending, then by endpoint name to ensure determinism if there's a tie
    # The prompt says "Sort them by frequency (descending)."
    # For ties, any order is generally acceptable, but we'll just check frequency logic.
    sorted_endpoints = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
    top_5 = [ep for ep, count in sorted_endpoints[:5]]

    return top_5, stratified_lines, error_counts

def test_script_installed_and_fixed():
    """Verify the script is installed and the perturbation is removed."""
    assert os.path.isfile(INSTALLED_SCRIPT_PATH), f"Installed script {INSTALLED_SCRIPT_PATH} is missing. Did you run make install?"
    assert os.access(INSTALLED_SCRIPT_PATH, os.X_OK), f"Installed script {INSTALLED_SCRIPT_PATH} is not executable."

    with open(INSTALLED_SCRIPT_PATH, "r") as f:
        content = f.read()

    assert "NR>10" not in content.replace(" ", ""), "The deliberate perturbation 'NR>10' is still present in the installed script."

def test_top_errors_file():
    """Verify the top_errors.txt file contains the correct top 5 endpoints."""
    assert os.path.isfile(TOP_ERRORS_PATH), f"{TOP_ERRORS_PATH} is missing."

    top_5, _, error_counts = get_expected_data()

    with open(TOP_ERRORS_PATH, "r") as f:
        actual_endpoints = [line.strip() for line in f if line.strip()]

    assert len(actual_endpoints) == 5, f"Expected exactly 5 endpoints in {TOP_ERRORS_PATH}, found {len(actual_endpoints)}."

    # Check that the frequencies of the actual top 5 match the expected top 5 frequencies
    expected_freqs = sorted([error_counts[ep] for ep in top_5], reverse=True)
    actual_freqs = sorted([error_counts.get(ep, 0) for ep in actual_endpoints], reverse=True)

    assert actual_freqs == expected_freqs, f"Top 5 endpoints in {TOP_ERRORS_PATH} do not match the expected frequencies."

def test_stratified_errors_file():
    """Verify the stratified_errors.tsv file contains exactly 2 logs per error endpoint."""
    assert os.path.isfile(STRATIFIED_ERRORS_PATH), f"{STRATIFIED_ERRORS_PATH} is missing."

    _, expected_stratified, _ = get_expected_data()

    with open(STRATIFIED_ERRORS_PATH, "r") as f:
        actual_stratified = [line.strip('\n') for line in f if line.strip('\n')]

    # Check that the lines match the expected stratified lines
    assert sorted(actual_stratified) == sorted(expected_stratified), f"Contents of {STRATIFIED_ERRORS_PATH} do not match the expected stratified output."

def test_http_server_health():
    """Verify the HTTP server responds to /health with 'OK'."""
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {SERVER_URL}/health: {e}")

    assert response.status_code == 200, f"Expected status code 200 for /health, got {response.status_code}"
    assert response.text.strip() == "OK", f"Expected body 'OK' for /health, got {response.text}"

def test_http_server_top_errors():
    """Verify the HTTP server responds to /top-errors with a JSON array of the top 5 endpoints."""
    try:
        response = requests.get(f"{SERVER_URL}/top-errors", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {SERVER_URL}/top-errors: {e}")

    assert response.status_code == 200, f"Expected status code 200 for /top-errors, got {response.status_code}"

    try:
        actual_json = response.json()
    except ValueError:
        pytest.fail(f"Response from /top-errors is not valid JSON. Body: {response.text}")

    assert isinstance(actual_json, list), "Expected a JSON array for /top-errors."
    assert len(actual_json) == 5, f"Expected exactly 5 elements in the JSON array, got {len(actual_json)}."

    top_5, _, error_counts = get_expected_data()
    expected_freqs = sorted([error_counts[ep] for ep in top_5], reverse=True)
    actual_freqs = sorted([error_counts.get(ep, 0) for ep in actual_json], reverse=True)

    assert actual_freqs == expected_freqs, f"JSON array from /top-errors does not contain the correct top 5 endpoints. Got: {actual_json}"