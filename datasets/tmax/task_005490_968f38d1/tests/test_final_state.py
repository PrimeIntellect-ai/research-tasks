# test_final_state.py

import os
import re
import pytest

def test_solution_file_exists_and_correct():
    solution_path = "/home/user/solution.txt"
    dump_path = "/home/user/crash_dump.bin"

    assert os.path.isfile(solution_path), f"File {solution_path} is missing."
    assert os.path.isfile(dump_path), f"File {dump_path} is missing."

    # Extract the malicious string from the crash dump dynamically
    with open(dump_path, "rb") as f:
        dump_content = f.read()

    match = re.search(b"(SENSOR_OVERFLOW_[A-Za-z0-9_]+)\x00", dump_content)
    assert match is not None, "Could not find the malicious sensor name in the crash dump."
    expected_sensor_name = match.group(1).decode('utf-8')

    with open(solution_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {solution_path}, but found {len(lines)}."

    assert lines[0] == expected_sensor_name, f"Line 1 of {solution_path} is incorrect. Expected '{expected_sensor_name}', got '{lines[0]}'."
    assert lines[1] == "2.000000", f"Line 2 of {solution_path} is incorrect. Expected '2.000000', got '{lines[1]}'."

def test_sensor_service_fixes_applied():
    source_path = "/home/user/sensor_service.c"
    assert os.path.isfile(source_path), f"File {source_path} is missing."

    with open(source_path, "r") as f:
        source_code = f.read()

    # Check for memory leak fix
    assert "free(" in source_code, "Memory leak does not appear to be fixed (no 'free' found)."

    # Check for race condition fix (mutex or atomic)
    has_mutex = "pthread_mutex_" in source_code
    has_atomic = "_Atomic" in source_code or "__atomic" in source_code or "__sync" in source_code
    assert has_mutex or has_atomic, "Race condition does not appear to be fixed (no mutex or atomic operations found)."

    # Check for buffer overflow fix
    assert "strcpy(" not in source_code or "strncpy(" in source_code or "snprintf(" in source_code, "Buffer overflow does not appear to be fixed (unsafe 'strcpy' still present without bounds checking)."