# test_final_state.py
import os
import subprocess
import pytest

def test_recovered_csv():
    csv_path = "/home/user/data/recovered.csv"
    assert os.path.isfile(csv_path), f"Expected recovered CSV file at {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "1600000000,1,25",
        "1600000005,2,42",
        "1600000010,1,18"
    ]

    assert lines == expected_lines, (
        f"Contents of {csv_path} are incorrect.\n"
        f"Expected:\n{expected_lines}\n"
        f"Got:\n{lines}"
    )

def test_sensor_logger_binary_fixed():
    binary_path = "/home/user/sensor_logger"
    assert os.path.isfile(binary_path), f"Binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

    # Run the binary with a negative value
    try:
        result = subprocess.run(
            [binary_path, "1600000020", "1", "-10"],
            capture_output=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The sensor_logger binary timed out, indicating a possible infinite loop or deadlock.")

    assert result.returncode == 0, (
        f"The sensor_logger binary crashed or returned non-zero exit code ({result.returncode}) "
        f"when run with a negative value.\n"
        f"Stderr: {result.stderr.decode('utf-8', errors='ignore')}"
    )

def test_sensor_logger_source_fixed():
    source_path = "/home/user/sensor_logger.c"
    assert os.path.isfile(source_path), f"Source file {source_path} is missing."

    with open(source_path, "r") as f:
        content = f.read()

    # The original buggy code had `if (val < 0) { free(r); }` before `r->value = val;`.
    # A correct fix would either remove the early free, or allocate differently.
    # We will do a basic check to ensure the file was modified from the original buggy state.
    original_bug_snippet = "if (val < 0) {\n        free(r); // BUG: Use after free\n    }"

    assert "BUG: Use after free" not in content or "if (val < 0)" not in content[:content.find("BUG: Use after free")], (
        "The source file still appears to contain the original use-after-free bug logic."
    )