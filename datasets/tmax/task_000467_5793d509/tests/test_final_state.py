# test_final_state.py

import os
import struct
import base64
import math

SECRET_KEY_PATH = "/home/user/secret.key"
REPORT_BIN_PATH = "/home/user/diagnostic_report.bin"
REPORT_B64_PATH = "/home/user/report.b64"

def test_secret_key_exists_and_correct():
    assert os.path.isfile(SECRET_KEY_PATH), f"Missing secret key file at {SECRET_KEY_PATH}"

    with open(SECRET_KEY_PATH, "r") as f:
        content = f.read().strip()

    try:
        secret_val = float(content)
    except ValueError:
        assert False, f"Content of {SECRET_KEY_PATH} is not a valid float: {content}"

    assert math.isclose(secret_val, 3.14159, rel_tol=1e-5), \
        f"Secret key value is incorrect. Expected ~3.14159, got {secret_val}"

def test_diagnostic_report_bin():
    assert os.path.isfile(REPORT_BIN_PATH), f"Missing binary report file at {REPORT_BIN_PATH}"

    with open(REPORT_BIN_PATH, "rb") as f:
        data = f.read()

    assert len(data) == 20, \
        f"Binary report file must be exactly 20 bytes long (5 floats). Got {len(data)} bytes."

    floats = struct.unpack('5f', data)

    inputs = [10.5, 20.2, 15.0, 8.8, 42.0]
    secret = 3.14159
    expected = [(val * secret) / 7.0 for val in inputs]

    for i in range(5):
        assert math.isclose(floats[i], expected[i], rel_tol=1e-4), \
            f"Value mismatch at index {i}: got {floats[i]}, expected {expected[i]}"

def test_report_b64():
    assert os.path.isfile(REPORT_B64_PATH), f"Missing base64 report file at {REPORT_B64_PATH}"
    assert os.path.isfile(REPORT_BIN_PATH), f"Missing binary report file at {REPORT_BIN_PATH} to compare against"

    with open(REPORT_BIN_PATH, "rb") as f:
        bin_data = f.read()

    expected_b64 = base64.b64encode(bin_data).decode('utf-8')

    with open(REPORT_B64_PATH, "r") as f:
        actual_b64 = f.read().strip()

    assert actual_b64 == expected_b64, \
        "Base64 file content does not match the base64 encoding of the binary file."