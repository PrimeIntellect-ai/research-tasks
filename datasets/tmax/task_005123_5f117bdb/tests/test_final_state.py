# test_final_state.py
import os
import json
import subprocess
import pytest

def fletcher16(data: bytes) -> int:
    sum1 = 0
    sum2 = 0
    for byte in data:
        sum1 = (sum1 + byte) % 255
        sum2 = (sum2 + sum1) % 255
    return (sum2 << 8) | sum1

def test_executable_exists():
    exe_path = "/home/user/project_sync/fast_checksum"
    assert os.path.isfile(exe_path), f"Executable {exe_path} not found. Did you compile the C++ code?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_api_payload_json():
    json_path = "/home/user/project_sync/api_payload.json"
    assert os.path.isfile(json_path), f"File {json_path} not found. Did you run the executable?"

    with open(json_path, 'r') as f:
        try:
            payload = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "files" in payload, "'files' key missing in JSON payload."

    data_dir = "/home/user/project_sync/data"
    expected_results = {}
    for fname in sorted(os.listdir(data_dir)):
        file_path = os.path.join(data_dir, fname)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as fp:
                expected_results[fname] = fletcher16(fp.read())

    assert payload["files"] == expected_results, (
        f"JSON payload does not match expected checksums.\n"
        f"Expected: {expected_results}\n"
        f"Got: {payload['files']}"
    )

def test_valgrind_memory_safety():
    exe_path = "/home/user/project_sync/fast_checksum"
    if not os.path.isfile(exe_path):
        pytest.fail("Executable missing, cannot run valgrind.")

    # Run valgrind to check for memory leaks and undefined behavior (like buffer overflows)
    cmd = [
        "valgrind",
        "--error-exitcode=1",
        "--leak-check=full",
        exe_path
    ]

    # Run the command from the project directory to ensure relative paths (if any) work correctly
    # though the C++ code uses absolute paths.
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/home/user/project_sync")

    assert result.returncode == 0, (
        f"Valgrind reported memory errors or leaks. Return code: {result.returncode}\n"
        f"Valgrind Output:\n{result.stderr}"
    )