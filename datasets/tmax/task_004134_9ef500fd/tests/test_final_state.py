# test_final_state.py
import os
import requests
import subprocess
import pytest

def test_hdf5_file_exists_and_valid():
    filepath = "/home/user/posterior.h5"
    assert os.path.exists(filepath), f"File {filepath} does not exist."

    # Check HDF5 signature
    with open(filepath, "rb") as f:
        header = f.read(8)
    assert header == b"\x89HDF\r\n\x1a\n", f"File {filepath} is not a valid HDF5 file."

    # Check dataset if h5ls is available
    try:
        result = subprocess.run(["h5ls", filepath], capture_output=True, text=True)
        if result.returncode == 0:
            assert "mcmc_chain" in result.stdout, "Dataset 'mcmc_chain' not found in HDF5 file."
            assert "10000" in result.stdout and "3" in result.stdout, "Dataset shape does not appear to be (10000, 3)."
    except FileNotFoundError:
        # h5ls not installed, rely on API tests to validate contents implicitly
        pass

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/api/v1/posterior_means"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized, got {response.status_code}. Response: {response.text}"

def test_api_authorized_and_values():
    url = "http://127.0.0.1:8080/api/v1/posterior_means"
    headers = {"X-API-Key": "bio-secret-994"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    for key in ["A", "B", "C"]:
        assert key in data, f"Key '{key}' is missing in the JSON response."

    # Check tolerances
    assert 140 <= data["A"] <= 160, f"Parameter A ({data['A']}) is out of the expected range (150 ± 10)."
    assert 1.2 <= data["B"] <= 1.8, f"Parameter B ({data['B']}) is out of the expected range (1.5 ± 0.3)."
    assert 15 <= data["C"] <= 25, f"Parameter C ({data['C']}) is out of the expected range (20 ± 5)."