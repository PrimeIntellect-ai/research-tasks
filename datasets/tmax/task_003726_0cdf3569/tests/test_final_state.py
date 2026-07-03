# test_final_state.py

import os
import subprocess
import pytest

def test_files_exist():
    """Check that all required files were created."""
    expected_files = [
        "/home/user/integrate_fixed.go",
        "/home/user/cpu.prof",
        "/home/user/partials.csv",
        "/home/user/partials.png",
        "/home/user/result.txt"
    ]
    for f in expected_files:
        assert os.path.exists(f), f"Expected file {f} is missing."
        assert os.path.isfile(f), f"Expected {f} to be a file."

def test_partials_csv_format():
    """Verify that partials.csv has 16 lines, ordered 0 to 15."""
    csv_path = "/home/user/partials.csv"
    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 16, f"Expected exactly 16 lines in {csv_path}, found {len(lines)}."

    for i, line in enumerate(lines):
        parts = line.split(",")
        assert len(parts) == 2, f"Line {i} in {csv_path} does not have exactly two comma-separated values: {line}"
        assert parts[0] == str(i), f"Expected line {i} to start with chunk ID {i}, got {parts[0]}."
        try:
            float(parts[1])
        except ValueError:
            pytest.fail(f"Expected a float for partial sum on line {i}, got {parts[1]}.")

def test_result_txt_format():
    """Verify that result.txt contains a valid float."""
    result_path = "/home/user/result.txt"
    with open(result_path, "r") as f:
        content = f.read().strip()

    try:
        float(content)
    except ValueError:
        pytest.fail(f"Expected a float in {result_path}, got {content}.")

def test_go_code_determinism_and_correctness():
    """Run the fixed Go code twice to ensure it is deterministic and matches result.txt."""
    go_file = "/home/user/integrate_fixed.go"

    # Run first time
    proc1 = subprocess.run(["go", "run", go_file], capture_output=True, text=True)
    assert proc1.returncode == 0, f"Go program failed to run: {proc1.stderr}"
    out1 = proc1.stdout.strip()

    # Run second time
    proc2 = subprocess.run(["go", "run", go_file], capture_output=True, text=True)
    assert proc2.returncode == 0, f"Go program failed to run on second attempt: {proc2.stderr}"
    out2 = proc2.stdout.strip()

    assert out1 == out2, "The Go program is not deterministic. Output differs between runs."

    # Check against result.txt
    result_path = "/home/user/result.txt"
    with open(result_path, "r") as f:
        saved_result = f.read().strip()

    assert out1 == saved_result, f"The output of the Go program ({out1}) does not match the contents of {result_path} ({saved_result})."