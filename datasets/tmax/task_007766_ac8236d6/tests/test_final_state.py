# test_final_state.py

import os
import json

def test_pipeline_output_exists():
    """Test that the pipeline output file was created."""
    output_file = "/home/user/pipeline_output.txt"
    assert os.path.isfile(output_file), f"Output file not found: {output_file}"

def test_pipeline_output_content():
    """Test that the pipeline output content matches the expected rolling averages and error formatting."""
    input_file = "/home/user/sensor_stream.jsonl"
    output_file = "/home/user/pipeline_output.txt"

    assert os.path.isfile(input_file), f"Input file not found: {input_file}"

    expected_lines = []
    window = []

    # Recompute the expected output from the input file
    with open(input_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            try:
                data = json.loads(line)
                window.append(data["temperature"])
                if len(window) > 3:
                    window.pop(0)
                avg = sum(window) / len(window)
                expected_lines.append(f"SUCCESS: Sensor {data['sensor_id']} processed. Rolling avg: {avg:.2f}")
            except Exception:
                expected_lines.append(f"ERROR: Line {i} failed validation")

    expected_output = "\n".join(expected_lines)

    with open(output_file, "r", encoding="utf-8") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Pipeline output does not match expected.\n"
        f"Expected:\n{expected_output}\n\n"
        f"Actual:\n{actual_output}"
    )