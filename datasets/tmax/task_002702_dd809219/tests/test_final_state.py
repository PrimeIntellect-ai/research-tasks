# test_final_state.py
import json
import os
import math

def test_analysis_result_exists():
    """Test that the analysis_result.json file was created in the correct location."""
    file_path = "/home/user/analysis_result.json"
    assert os.path.isfile(file_path), f"Expected output file is missing: {file_path}"

def test_analysis_result_format_and_content():
    """Test that the JSON file has the correct keys and expected values."""
    file_path = "/home/user/analysis_result.json"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "analysis_result.json is not a valid JSON file."

    # Check for required keys
    assert "sequence" in data, "The key 'sequence' is missing from the JSON output."
    assert "ks_pvalue" in data, "The key 'ks_pvalue' is missing from the JSON output."

    # Validate the reconstructed sequence
    expected_sequence = "A-G-C-T-A-A-T-G-C-C"
    actual_sequence = data["sequence"]
    assert actual_sequence == expected_sequence, (
        f"Sequence mismatch. Expected '{expected_sequence}', but got '{actual_sequence}'."
    )

    # Validate the KS test p-value
    # The expected p-value based on the deterministic seed and data generation is approximately 0.8166
    expected_pvalue = 0.8166
    actual_pvalue = data["ks_pvalue"]

    assert isinstance(actual_pvalue, (int, float)), "ks_pvalue must be a number."

    assert math.isclose(actual_pvalue, expected_pvalue, abs_tol=0.0005), (
        f"KS p-value mismatch. Expected approximately {expected_pvalue}, "
        f"but got {actual_pvalue}. Ensure you used the correct seed, filtering logic, and statistical test."
    )