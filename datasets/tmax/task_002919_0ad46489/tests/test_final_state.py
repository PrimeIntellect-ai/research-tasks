# test_final_state.py

import os
import re
import pytest

def test_extractor_cpp_exists():
    """Check that the C++ source file exists."""
    path = "/home/user/extractor.cpp"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_extractor_executable_exists():
    """Check that the compiled extractor exists and is executable."""
    path = "/home/user/extractor"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_process_sh_exists_and_executable():
    """Check that the bash script exists and is executable."""
    path = "/home/user/process.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_top_cpu_csv_contents():
    """Check that top_cpu.csv contains the correct top 5 records."""
    path = "/home/user/top_cpu.csv"
    assert os.path.isfile(path), f"File {path} does not exist."

    expected_lines = [
        "1696151040,srv-04,99",
        "1696151280,srv-04,95",
        "1696150860,srv-02,92",
        "1696150920,srv-01,88",
        "1696151160,srv-05,78"
    ]

    with open(path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {path} do not match the expected output. Got: {actual_lines}"

def test_cron_configuration():
    """Check that telemetry.cron contains the correct cron expression."""
    path = "/home/user/telemetry.cron"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    # Look for the specific cron job
    pattern = r"^0\s+\*\s+\*\s+\*\s+\*\s+/bin/bash\s+/home/user/process\.sh"

    found = False
    for line in content.splitlines():
        if re.match(pattern, line.strip()):
            found = True
            break

    assert found, f"Cron expression for process.sh at minute 0 not found in {path}."