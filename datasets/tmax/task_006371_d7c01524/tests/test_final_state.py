# test_final_state.py
import os
import json
import math

def test_analysis_json_exists():
    """Verify that the analysis.json file was created in the correct location."""
    assert os.path.isfile('/home/user/analysis.json'), "/home/user/analysis.json does not exist."

def test_analysis_json_contents():
    """Verify the contents of the analysis.json file match the expected values within tolerance."""
    with open('/home/user/analysis.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "/home/user/analysis.json is not a valid JSON file."

    assert "total_mrna_integral" in data, "Missing 'total_mrna_integral' in JSON output."
    assert "dominant_frequency_hz" in data, "Missing 'dominant_frequency_hz' in JSON output."

    integral = data["total_mrna_integral"]
    freq = data["dominant_frequency_hz"]

    assert isinstance(integral, (int, float)), "'total_mrna_integral' must be a number."
    assert isinstance(freq, (int, float)), "'dominant_frequency_hz' must be a number."

    expected_integral = 1635.805
    expected_freq = 0.0249875

    assert math.isclose(integral, expected_integral, rel_tol=0.01), \
        f"'total_mrna_integral' {integral} is not within 1% of expected value {expected_integral}."
    assert math.isclose(freq, expected_freq, rel_tol=0.05), \
        f"'dominant_frequency_hz' {freq} is not within 5% of expected value {expected_freq}."