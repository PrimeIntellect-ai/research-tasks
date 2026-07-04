# test_final_state.py

import os
import subprocess
import pytest

def test_pipeline_execution_and_output():
    script_path = "/home/user/pipeline/run.sh"
    assert os.path.isfile(script_path), f"Script not found: {script_path}"

    # Execute the pipeline script
    result = subprocess.run(
        ["bash", script_path],
        cwd="/home/user/pipeline",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"run.sh failed to execute. stderr: {result.stderr}"

    output_file = "/home/user/pipeline/output/results.txt"
    assert os.path.isfile(output_file), f"Output file not generated at expected path: {output_file}"

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines of output, but got {len(lines)}: {lines}"

    # Verify no floating point anomalies are present in the strings
    for i, line in enumerate(lines, start=1):
        assert "0.30000000000000004" not in line, f"Floating point anomaly found in output line {i}: {line}"

    # Extract the summed values
    try:
        val1 = lines[0].split(":")[1].strip()
        val2 = lines[1].split(":")[1].strip()
        val3 = lines[2].split(":")[1].strip()
    except IndexError:
        pytest.fail(f"Output lines are not formatted as 'Packet <N>: <Sum>'. Got: {lines}")

    # Verify string representations to ensure precision correctness
    assert val1 in ["0.3", "0.30"], f"Packet 1 value incorrect or imprecise: {val1}"
    assert val2 in ["0.3", "0.30"], f"Packet 2 value incorrect or imprecise: {val2}"
    assert val3 in ["0.8", "0.80"], f"Packet 3 value incorrect or imprecise: {val3}"

    # Verify prefix formatting
    assert lines[0].startswith("Packet 1:"), f"Line 1 prefix incorrect: {lines[0]}"
    assert lines[1].startswith("Packet 2:"), f"Line 2 prefix incorrect: {lines[1]}"
    assert lines[2].startswith("Packet 3:"), f"Line 3 prefix incorrect: {lines[2]}"