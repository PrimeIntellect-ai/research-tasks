# test_final_state.py

import os
import json
import math

def test_analysis_results_exists():
    path = '/home/user/analysis_results.json'
    assert os.path.isfile(path), f"The output file {path} is missing. Ensure you ran the compiled tool and generated the output."

def test_analysis_results_content():
    path = '/home/user/analysis_results.json'
    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {path} is not valid JSON."

    assert "total_entries" in data, "The JSON output is missing the 'total_entries' field."
    assert "decoded_bytes_count" in data, "The JSON output is missing the 'decoded_bytes_count' field."
    assert "variance" in data, "The JSON output is missing the 'variance' field."

    # Verify boundary condition fix
    expected_entries = 1000
    actual_entries = data["total_entries"]
    assert actual_entries == expected_entries, (
        f"Expected 'total_entries' to be {expected_entries}, but got {actual_entries}. "
        "Check if the boundary condition bug is fully fixed."
    )

    # Verify hex decoding fix
    expected_bytes = 14890
    actual_bytes = data["decoded_bytes_count"]
    assert actual_bytes == expected_bytes, (
        f"Expected 'decoded_bytes_count' to be {expected_bytes}, but got {actual_bytes}. "
        "Check if the hex decoding correctly handles both uppercase and lowercase letters."
    )

    # Verify numerical stability fix
    expected_variance = 0.00000825
    actual_variance = float(data["variance"])
    assert math.isclose(actual_variance, expected_variance, abs_tol=1e-10), (
        f"Expected 'variance' to be close to {expected_variance}, but got {actual_variance}. "
        "Check if you implemented a numerically stable variance algorithm (like Welford's)."
    )