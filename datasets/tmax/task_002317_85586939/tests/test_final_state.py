# test_final_state.py

import os
import math

def test_output_file_exists_and_correct():
    output_path = "/home/user/output.txt"
    assert os.path.isfile(output_path), f"Output file does not exist: {output_path}"

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "154.50", f"Output file contains incorrect value: {content}. Expected: 154.50"

def test_sensor_data_unchanged():
    data_path = "/home/user/sensor_data.txt"
    assert os.path.isfile(data_path), f"Input data file missing: {data_path}"

    with open(data_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) == 105, f"Input data file length changed. Expected 105, got {len(lines)}"
    assert lines[0] == "1e16", "Input data file first line changed."
    assert lines[-1] == "-1e16", "Input data file last line changed."

    # Check that the mathematical sum of the file is still 154.50
    floats = [float(x) for x in lines]
    assert math.isclose(math.fsum(floats), 154.50), "Input data file contents changed."

def test_sensor_aggregator_exists():
    script_path = "/home/user/sensor_aggregator.py"
    assert os.path.isfile(script_path), f"Missing script file: {script_path}"