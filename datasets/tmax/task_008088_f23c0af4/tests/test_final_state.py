# test_final_state.py
import os
import json
import glob
import pytest

def calc_expected_checksum(size, fill):
    checksum = 0x12345678
    for _ in range(size):
        checksum ^= fill
        checksum = ((checksum << 1) & 0xFFFFFFFF) | (checksum >> 31)
    return f"{checksum:08x}"

def test_verifier_c_fixed():
    filepath = "/home/user/src/verifier.c"
    assert os.path.isfile(filepath), f"Source file {filepath} is missing"

    with open(filepath, "r") as f:
        content = f.read()

    # The loop should not have <= length
    assert "i <= length" not in content, "Bug 1 (loop boundary) was not fixed in verifier.c"

    # There should not be a double free
    assert content.count("free(buffer);") == 1, "Bug 2 (double free) was not fixed in verifier.c, or buffer is not freed exactly once"

def test_executable_exists():
    filepath = "/home/user/bin/verifier"
    assert os.path.isfile(filepath), f"Executable {filepath} is missing"
    assert os.access(filepath, os.X_OK), f"File {filepath} is not executable"

def test_packaging_script_exists():
    scripts = glob.glob("/home/user/package_artifacts.*")
    assert len(scripts) > 0, "Packaging script /home/user/package_artifacts.* is missing"

def test_verified_checksums_json():
    filepath = "/home/user/verified_checksums.json"
    assert os.path.isfile(filepath), f"JSON report {filepath} is missing"

    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{filepath} is not a valid JSON file")

    expected_checksums = {
        "app_v1.bin": calc_expected_checksum(1024, 0xAA),
        "app_v2.bin": calc_expected_checksum(2048, 0xBB),
        "app_v3.bin": calc_expected_checksum(512, 0xCC)
    }

    assert isinstance(data, dict), "JSON root must be an object (dictionary)"

    for filename, expected_hex in expected_checksums.items():
        assert filename in data, f"Missing key '{filename}' in {filepath}"

        # Extract the exact hex string, case-insensitive check
        actual_hex = str(data[filename]).strip().lower()
        # Some students might include the filename in the value if they just split poorly, but the spec says "exact hexadecimal string"
        # We can just check if actual_hex ends with or equals the expected hex.
        # But let's strictly check equality as per spec: "values are the exact hexadecimal string output by the verifier"

        # The verifier output is "%s: %08x\n", so the exact hex is just the %08x part.
        assert actual_hex == expected_hex.lower(), f"Checksum for {filename} is incorrect. Expected {expected_hex.lower()}, got {actual_hex}"