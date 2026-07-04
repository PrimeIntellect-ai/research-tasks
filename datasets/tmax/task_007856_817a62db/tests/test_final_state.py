# test_final_state.py

import os
import subprocess
import math

def test_buggy_line_identified():
    """Verify that the buggy line number was correctly identified and written to buggy_line.txt."""
    buggy_file = "/home/user/buggy_line.txt"
    assert os.path.isfile(buggy_file), f"File {buggy_file} does not exist."

    with open(buggy_file, "r") as f:
        content = f.read().strip()

    assert content == "3421", f"Expected buggy line to be 3421, but found '{content}'."

def test_calc_variance_script_output():
    """Verify that the fixed script calculates the correct population variance without crashing."""
    script_path = "/home/user/calc_variance.sh"
    csv_path = "/home/user/daily_query.csv"

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Compute the expected variance in Python to ensure correctness
    vals = []
    with open(csv_path, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 3 and parts[1] == "SENSOR_X":
                try:
                    vals.append(float(parts[2]))
                except ValueError:
                    pass

    assert len(vals) > 0, "No valid sensor readings found."

    mean = sum(vals) / len(vals)
    variance = sum((x - mean) ** 2 for x in vals) / len(vals)
    expected_variance = math.floor(variance)

    # Run the student's script
    result = subprocess.run(
        [script_path, csv_path, "SENSOR_X"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script crashed or returned non-zero exit code. STDERR: {result.stderr}"

    output = result.stdout.strip()
    assert output, "Script produced no output."

    try:
        student_variance = int(output)
    except ValueError:
        pytest.fail(f"Script output '{output}' is not a valid integer.")

    assert student_variance == expected_variance, (
        f"Incorrect variance calculated. Expected {expected_variance}, got {student_variance}."
    )