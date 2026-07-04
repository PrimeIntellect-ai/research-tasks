# test_final_state.py

import os
import subprocess
import pytest

def test_crash_value_file():
    path = "/home/user/crash_value.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "-1.5", f"Expected crash_value.txt to contain '-1.5', but found '{content}'."

def test_executable_exists():
    path = "/home/user/telemetry_service/telemetry"
    assert os.path.exists(path), f"Executable {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_executable_runs_successfully():
    executable = "/home/user/telemetry_service/telemetry"
    input_file = "/home/user/telemetry_service/input.bin"

    assert os.path.exists(executable), f"Executable {executable} is missing."
    assert os.path.exists(input_file), f"Input file {input_file} is missing."

    try:
        result = subprocess.run(
            [executable, input_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The telemetry executable timed out during execution.")
    except Exception as e:
        pytest.fail(f"Failed to run the telemetry executable: {e}")

    assert result.returncode == 0, (
        f"Expected exit code 0, but got {result.returncode}.\n"
        f"STDOUT: {result.stdout.decode('utf-8', errors='ignore')}\n"
        f"STDERR: {result.stderr.decode('utf-8', errors='ignore')}"
    )