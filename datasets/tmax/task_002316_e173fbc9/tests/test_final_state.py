# test_final_state.py

import os
import sys
import tempfile
import pytest
import requests
import pandas as pd

def test_preprocess_fixed():
    """Verify the bug in textprep_lib is fixed and it handles 'None' correctly."""
    # Add to sys.path to ensure we can import it even if not installed globally
    sys.path.insert(0, "/app/textprep_lib-0.4.5")
    try:
        from textprep_lib.preprocess import load_and_clean
    except ImportError:
        pytest.fail("Could not import textprep_lib.preprocess. Was it fixed and structured correctly?")

    # Create a dummy CSV to test the function
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("abstract,citations,is_accepted\n")
        f.write("test paper 1,None,1\n")
        f.write("test paper 2,5,0\n")
        temp_path = f.name

    try:
        df = load_and_clean(temp_path)
        assert 'citations' in df.columns, "citations column missing after load_and_clean"

        # Check if 'None' was replaced by 0
        assert df.loc[0, 'citations'] == 0, "String 'None' was not replaced by 0"

        # Check if column is integer
        assert pd.api.types.is_integer_dtype(df['citations']), f"citations column is not integer type, got {df['citations'].dtype}"
    finally:
        os.remove(temp_path)

def test_cv_result_exists_and_valid():
    """Verify the CV result file exists and contains a valid float."""
    path = "/home/user/cv_result.txt"
    assert os.path.isfile(path), f"CV result file {path} is missing."

    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"CV result file does not contain a valid float. Found: {content}")

    assert 0.0 <= val <= 1.0, f"CV accuracy should be between 0.0 and 1.0, got {val}"

def test_web_service_auth_missing():
    """Verify the web service rejects requests without authorization."""
    url = "http://127.0.0.1:5000/predict"
    payload = {"abstract": "A novel framework for...", "citations": 12}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the web service at {url}: {e}")

    assert response.status_code in (401, 403), f"Expected 401 or 403 for missing auth, got {response.status_code}"

def test_web_service_auth_wrong():
    """Verify the web service rejects requests with incorrect authorization."""
    url = "http://127.0.0.1:5000/predict"
    payload = {"abstract": "A novel framework for...", "citations": 12}
    headers = {"Authorization": "Bearer wrong-token"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the web service at {url}: {e}")

    assert response.status_code in (401, 403), f"Expected 401 or 403 for wrong auth, got {response.status_code}"

def test_web_service_success():
    """Verify the web service returns a valid prediction with correct auth and payload."""
    url = "http://127.0.0.1:5000/predict"
    payload = {"abstract": "A novel framework for deep learning models.", "citations": 42}
    headers = {"Authorization": "Bearer ds-research-token-881"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the web service at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "prediction" in data, f"Key 'prediction' missing from response JSON: {data}"
    assert data["prediction"] in (0, 1), f"Prediction value should be 0 or 1, got {data['prediction']}"