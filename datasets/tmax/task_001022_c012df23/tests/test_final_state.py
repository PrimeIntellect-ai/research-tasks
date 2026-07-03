# test_final_state.py

import os
import pytest

def test_anomaly_score_metric():
    """Check that the anomaly score is computed correctly within the tolerance."""
    output_file = "/home/user/service/anomaly_score.txt"

    # Check that the output file exists
    assert os.path.isfile(output_file), f"Output file missing: {output_file}. Did you run the pipeline?"

    # Read the contents
    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content, f"Output file {output_file} is empty."

    # Parse the float
    try:
        score = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {output_file} as a float. Found: {content}")

    # Check the metric
    target_value = 7071.06
    tolerance = 0.1
    difference = abs(score - target_value)

    assert difference <= tolerance, (
        f"Anomaly score {score} is not within {tolerance} of the target {target_value}. "
        f"Difference is {difference}."
    )