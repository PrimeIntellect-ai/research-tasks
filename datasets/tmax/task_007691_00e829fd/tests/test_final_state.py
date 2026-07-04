# test_final_state.py
import os
import struct

def test_recovered_log_exists_and_correct():
    bin_path = "/home/user/telemetry.bin"
    log_path = "/home/user/recovered.log"

    assert os.path.isfile(bin_path), f"Expected binary file {bin_path} to exist."
    assert os.path.isfile(log_path), f"Expected log file {log_path} to exist."

    # Compute expected output based on the binary file
    with open(bin_path, 'rb') as f:
        data = f.read()

    assert len(data) >= 1, "Binary file is empty."

    length = data[0]
    assert len(data) >= 1 + length + 8, "Binary file is too short to contain the expected payload."

    device_name = data[1:1+length].decode('utf-8')
    val = struct.unpack('>d', data[1+length:1+length+8])[0]

    expected_content = f"Device: {device_name}, Value: {val}"

    with open(log_path, 'r', encoding='utf-8') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {log_path} is incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Got: '{actual_content}'"
    )