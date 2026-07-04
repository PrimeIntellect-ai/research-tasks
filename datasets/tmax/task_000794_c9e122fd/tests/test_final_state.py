# test_final_state.py
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"

def test_barcode_endpoint():
    """Test the /barcode endpoint returns the correct 12-nucleotide sequence."""
    try:
        response = requests.get(f"{BASE_URL}/barcode", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/barcode: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    actual_barcode = response.text.strip()
    expected_barcode = "ACGTAACCGGTT"
    assert actual_barcode == expected_barcode, f"Expected barcode '{expected_barcode}', got '{actual_barcode}'"

def test_consensus_endpoint():
    """Test the /consensus endpoint returns the correctly assembled sequence."""
    try:
        response = requests.get(f"{BASE_URL}/consensus", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/consensus: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    actual_consensus = response.text.strip()
    expected_consensus = "ACGTAACCGGTTATGCATGC"
    assert actual_consensus == expected_consensus, f"Expected consensus '{expected_consensus}', got '{actual_consensus}'"

def test_error_rate_endpoint():
    """Test the /error_rate endpoint returns a float within the acceptable MCMC posterior mean range."""
    try:
        response = requests.get(f"{BASE_URL}/error_rate", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/error_rate: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    raw_text = response.text.strip()
    try:
        error_rate = float(raw_text)
    except ValueError:
        pytest.fail(f"Expected a float for error_rate, got '{raw_text}'")

    assert 0.030 <= error_rate <= 0.045, f"Expected error_rate between 0.030 and 0.045, got {error_rate}"