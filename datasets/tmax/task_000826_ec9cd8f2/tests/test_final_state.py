# test_final_state.py

import os
import pytest

def djb2_64(s):
    hash_val = 5381
    for char in s:
        hash_val = ((hash_val << 5) + hash_val + ord(char)) & 0xFFFFFFFFFFFFFFFF
    return hash_val

def djb2_32(s):
    hash_val = 5381
    for char in s:
        hash_val = ((hash_val << 5) + hash_val + ord(char)) & 0xFFFFFFFF
    return hash_val

def test_c_program_exists():
    assert os.path.isfile("/home/user/align_hash.c"), "C source file /home/user/align_hash.c is missing."

def test_executable_exists():
    assert os.path.isfile("/home/user/align_hash"), "Executable /home/user/align_hash is missing."
    assert os.access("/home/user/align_hash", os.X_OK), "/home/user/align_hash is not executable."

def test_bash_script_exists():
    assert os.path.isfile("/home/user/run_pipeline.sh"), "Bash script /home/user/run_pipeline.sh is missing."

def test_final_output_exists_and_correct():
    output_file = "/home/user/final_output.csv"
    assert os.path.isfile(output_file), f"Final output file {output_file} is missing."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {output_file}, found {len(lines)}."

    expected_64 = [
        f"2023-10-25T14:32:00Z,S1,{djb2_64('battery_low')}",
        f"2023-10-25T14:35:00Z,S2,{djb2_64('temp_high')}",
        f"2023-10-25T14:40:00Z,S1,{djb2_64('rebooting')}"
    ]

    expected_32 = [
        f"2023-10-25T14:32:00Z,S1,{djb2_32('battery_low')}",
        f"2023-10-25T14:35:00Z,S2,{djb2_32('temp_high')}",
        f"2023-10-25T14:40:00Z,S1,{djb2_32('rebooting')}"
    ]

    expected_64.sort()
    expected_32.sort()

    is_64_match = lines == expected_64
    is_32_match = lines == expected_32

    if not (is_64_match or is_32_match):
        # Provide detailed feedback if it doesn't match perfectly
        for idx, line in enumerate(lines):
            parts = line.split(',')
            assert len(parts) == 3, f"Line {idx+1} does not have exactly 3 comma-separated fields: {line}"

            ts, sid, hash_val = parts
            assert ts.endswith("00Z"), f"Timestamp not correctly aligned to minute in line {idx+1}: {ts}"
            assert hash_val.isdigit(), f"Hash value is not numeric in line {idx+1}: {hash_val}"

        pytest.fail(f"File contents do not match expected sorted output. Found: {lines}")