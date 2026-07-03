# test_final_state.py

import os
import subprocess
import pytest

def test_decoder_cpp_exists():
    path = "/home/user/decoder.cpp"
    assert os.path.isfile(path), f"C++ source file {path} does not exist. Did you write the program?"

def test_decoder_executable_exists():
    path = "/home/user/decoder"
    assert os.path.isfile(path), f"Executable file {path} does not exist. Did you compile your program?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_fingerprint_file_correct():
    cert_path = "/home/user/isolated_env/tmp/rogue.crt"
    fingerprint_path = "/home/user/fingerprint.txt"

    assert os.path.isfile(cert_path), f"Rogue certificate {cert_path} is missing."
    assert os.path.isfile(fingerprint_path), f"Result file {fingerprint_path} does not exist. Did you save the fingerprint?"

    # Compute expected fingerprint
    try:
        result = subprocess.run(
            ["openssl", "x509", "-in", cert_path, "-noout", "-fingerprint", "-sha256"],
            capture_output=True,
            text=True,
            check=True
        )
        expected_fingerprint = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected fingerprint using openssl: {e}")

    # Read student's fingerprint
    with open(fingerprint_path, "r") as f:
        actual_fingerprint = f.read().strip()

    assert actual_fingerprint == expected_fingerprint, (
        f"The fingerprint in {fingerprint_path} is incorrect.\n"
        f"Expected: {expected_fingerprint}\n"
        f"Found: {actual_fingerprint}"
    )