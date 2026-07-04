# test_final_state.py

import os

def test_decoded_bin_exists_and_correct():
    """Verify that decoded.bin exists and contains the correct decrypted payload."""
    decoded_bin_path = "/home/user/decoded.bin"
    assert os.path.isfile(decoded_bin_path), f"File {decoded_bin_path} is missing. The payload was not dropped."

    with open(decoded_bin_path, "r", encoding="utf-8") as f:
        contents = f.read()

    expected_contents = "RED_TEAM_STRIKES_AGAIN_WITH_C++!"
    assert contents == expected_contents, f"Contents of {decoded_bin_path} are incorrect. Got {contents!r}, expected {expected_contents!r}."

def test_evader_cpp_exists_and_uses_openssl():
    """Verify that evader.cpp exists and uses the OpenSSL certificate verification API."""
    cpp_path = "/home/user/evader.cpp"
    assert os.path.isfile(cpp_path), f"Source file {cpp_path} is missing."

    with open(cpp_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    assert "X509_verify_cert" in code, f"Source file {cpp_path} does not appear to use X509_verify_cert."

def test_evader_binary_exists():
    """Verify that the compiled evader binary exists and is executable."""
    bin_path = "/home/user/evader"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."