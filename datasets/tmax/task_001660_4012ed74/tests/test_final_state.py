# test_final_state.py
import os
import glob
import wave
import requests
import re

def test_shared_library_exists():
    lib_path = "/app/lib/libfingerprint.so"
    assert os.path.exists(lib_path), f"Shared library not found at {lib_path}"
    assert os.path.isfile(lib_path), f"{lib_path} is not a file"
    # Basic check for ELF file
    with open(lib_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{lib_path} is not a valid ELF shared object"

def test_property_based_test_exists():
    # Look for files matching /app/tests/test_ffi*
    files = glob.glob("/app/tests/test_ffi*")
    assert len(files) > 0, "No property-based test file found starting with /app/tests/test_ffi"

    # Check if any file contains common property-based testing imports
    found_import = False
    for fpath in files:
        if os.path.isfile(fpath):
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "hypothesis" in content or "gopter" in content or "rapidcheck" in content or "quickcheck" in content or "proptest" in content:
                    found_import = True
                    break
    assert found_import, "No property-based testing library imports (e.g., hypothesis, gopter) found in /app/tests/test_ffi*"

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/analyze"
    payload = {
        "token": "invalid",
        "filepath": "/app/audio/alert.wav"
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to API: {e}"

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_api_success_and_logic():
    url = "http://127.0.0.1:8080/analyze"
    filepath = "/app/audio/alert.wav"
    payload = {
        "token": "ci-token-992",
        "filepath": filepath
    }
    try:
        response = requests.post(url, json=payload, timeout=30)
    except requests.RequestException as e:
        assert False, f"Failed to connect to API: {e}"

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert data.get("status") == "success", "Expected status to be 'success'"

    # Compute the expected checksum
    assert os.path.exists(filepath), f"Audio fixture missing: {filepath}"
    try:
        with wave.open(filepath, "rb") as w:
            frames = w.readframes(w.getnframes())
    except Exception as e:
        assert False, f"Failed to read WAV file: {e}"

    expected_checksum = sum(frames) % 99991

    assert "checksum" in data, "Response missing 'checksum'"
    assert data["checksum"] == expected_checksum, f"Expected checksum {expected_checksum}, got {data['checksum']}"

    assert "transcription" in data, "Response missing 'transcription'"
    transcription = data["transcription"].lower()
    transcription_clean = re.sub(r'[^\w\s]', '', transcription)

    expected_words = ["build", "pipeline", "failed", "at", "network", "module"]
    for word in expected_words:
        assert word in transcription_clean, f"Expected word '{word}' not found in transcription: {data['transcription']}"