# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_mre_script_exists_and_runs():
    """Check that /home/user/mre.py exists and runs successfully."""
    mre_path = "/home/user/mre.py"
    assert os.path.exists(mre_path), f"Missing required file: {mre_path}"
    assert os.path.isfile(mre_path), f"Path is not a file: {mre_path}"

    try:
        result = subprocess.run(["python3", mre_path], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"mre.py failed to run. Output: {result.stderr}"
        assert "SUCCESS:" in result.stdout, "mre.py did not print 'SUCCESS: <extracted_text>'"
    except subprocess.TimeoutExpired:
        pytest.fail("mre.py execution timed out.")

def test_service_unauthorized():
    """Check that the service rejects requests without the proper auth header."""
    url = "http://127.0.0.1:8080/process"
    image_path = "/app/customer_upload.png"

    assert os.path.exists(image_path), f"Test image missing at {image_path}"

    with open(image_path, "rb") as f:
        files = {"file": f}
        try:
            response = requests.post(url, files=files, timeout=5)
            assert response.status_code in (401, 403), f"Expected 401 or 403 for missing auth, got {response.status_code}"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to the service: {e}")

def test_service_authorized_process():
    """Check that the service processes the image correctly with the proper auth header."""
    url = "http://127.0.0.1:8080/process"
    image_path = "/app/customer_upload.png"
    headers = {"Authorization": "Bearer diag-token-xyz"}

    assert os.path.exists(image_path), f"Test image missing at {image_path}"

    with open(image_path, "rb") as f:
        # Send as raw binary or multipart
        # Try multipart first
        files = {"file": f}
        try:
            response = requests.post(url, headers=headers, files=files, timeout=10)

            # If 400 or 500, maybe it expects raw binary
            if response.status_code not in (200, 201):
                f.seek(0)
                response = requests.post(url, headers=headers, data=f.read(), timeout=10)

            assert response.status_code in (200, 201), f"Expected success status code, got {response.status_code}. Response: {response.text}"

            data = response.json()
            assert "extracted_text" in data, "Response JSON missing 'extracted_text' key"

            extracted_text = data["extracted_text"]
            assert "O'Reilly" in extracted_text, f"Expected 'O'Reilly' in extracted text, got: {extracted_text}"

        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to the service or process request: {e}")
        except ValueError:
            pytest.fail(f"Response was not valid JSON. Response text: {response.text}")