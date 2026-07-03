# test_final_state.py

import os
import pytest

def test_final_average_accuracy():
    """
    Validates that the final average computed by the aggregator service
    meets the required accuracy threshold, ensuring both the ingestion 
    data loss and floating-point precision issues are resolved.
    """
    output_file = "/home/user/final_average.txt"

    # Check if the output file exists
    assert os.path.isfile(output_file), (
        f"Output file '{output_file}' does not exist. "
        "Did you successfully recompile the services, run '/app/start.sh', "
        "and execute '/app/test_harness.sh'?"
    )

    # Read the output file
    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content, f"Output file '{output_file}' is empty."

    # Parse the output as a float
    try:
        output_avg = float(content)
    except ValueError:
        pytest.fail(
            f"Could not parse the content of '{output_file}' as a float. "
            f"Content found: '{content}'"
        )

    # Calculate the metric (absolute error)
    true_avg = 1000000.00005
    error = abs(true_avg - output_avg)

    # Assert against the threshold
    threshold = 0.0001
    assert error < threshold, (
        f"Absolute error {error} is not strictly less than the threshold {threshold}. "
        f"The computed average was {output_avg}, but the expected true average is {true_avg}. "
        "Ensure that the ingest service successfully parses all payloads and the aggregator "
        "uses a numerically stable algorithm (e.g., float64, Kahan summation)."
    )