# test_final_state.py

import os

def calc_expected_checksum(filepath, size):
    with open(filepath, 'rb') as f:
        data = f.read(size)
    checksum = 0
    for byte in data:
        checksum = (((checksum << 1) | (checksum >> 7)) & 0xFF)
        checksum ^= byte
    return checksum

def test_executable_exists():
    executable_path = "/home/user/calc_hash"
    assert os.path.isfile(executable_path), f"Compiled executable missing: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File is not executable: {executable_path}"

def test_hash_output_correct():
    output_file = "/home/user/hash_output.txt"
    firmware_file = "/home/user/firmware.bin"

    assert os.path.isfile(output_file), f"Output file missing: {output_file}"
    assert os.path.isfile(firmware_file), f"Firmware file missing: {firmware_file}"

    # Calculate the expected checksum using the reference logic
    size = 512 * 7 + 13
    expected_checksum = calc_expected_checksum(firmware_file, size)
    expected_output = f"{expected_checksum}\n"

    with open(output_file, 'r') as f:
        actual_output = f.read()

    assert actual_output == expected_output, (
        f"Output in {output_file} is incorrect. "
        f"Expected '{expected_output.strip()}', got '{actual_output.strip()}'"
    )