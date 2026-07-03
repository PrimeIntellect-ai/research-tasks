# test_final_state.py
import requests
import pytest
import re

BASE_URL = "http://127.0.0.1:8080"

def test_convergence_endpoint():
    """Test the /convergence endpoint returns the correct frame number."""
    try:
        response = requests.get(f"{BASE_URL}/convergence", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/convergence: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    body = response.text.strip()
    assert body == "7", f"Expected convergence frame '7', got '{body}'"

def test_intensities_endpoint():
    """Test the /intensities endpoint returns the correct format and values within tolerance."""
    try:
        response = requests.get(f"{BASE_URL}/intensities", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/intensities: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    body = response.text.strip()

    # Expected format: TL=120.50,TR=49.00,BL=81.50,BR=199.00
    pattern = r"^TL=([0-9.]+),TR=([0-9.]+),BL=([0-9.]+),BR=([0-9.]+)$"
    match = re.match(pattern, body)
    assert match is not None, f"Response body '{body}' does not match expected format 'TL=<val>,TR=<val>,BL=<val>,BR=<val>'"

    tl, tr, bl, br = map(float, match.groups())

    # Expected values
    expected_tl = 120.50
    expected_tr = 49.00
    expected_bl = 81.50
    expected_br = 199.00

    tolerance = 1.0

    assert abs(tl - expected_tl) <= tolerance, f"TL value {tl} is outside tolerance of {expected_tl}"
    assert abs(tr - expected_tr) <= tolerance, f"TR value {tr} is outside tolerance of {expected_tr}"
    assert abs(bl - expected_bl) <= tolerance, f"BL value {bl} is outside tolerance of {expected_bl}"
    assert abs(br - expected_br) <= tolerance, f"BR value {br} is outside tolerance of {expected_br}"