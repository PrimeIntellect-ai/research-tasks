# test_final_state.py
import json
import os

def test_regression_report():
    report_path = "/home/user/regression_report.json"
    assert os.path.exists(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {report_path} does not contain valid JSON."

    assert "computed_mean" in data, "Missing 'computed_mean' in JSON."
    assert "reference_mean" in data, "Missing 'reference_mean' in JSON."
    assert "status" in data, "Missing 'status' in JSON."

    assert data["reference_mean"] == 2.62, f"Reference mean is {data['reference_mean']}, expected 2.62."

    computed = data["computed_mean"]
    assert isinstance(computed, (int, float)), "'computed_mean' must be a number."
    assert abs(computed - 2.62) <= 0.05, f"Computed mean {computed} is out of expected bounds (2.62 +/- 0.05)."
    assert computed == round(computed, 2), f"Computed mean {computed} should be rounded to exactly 2 decimal places."

    assert data["status"] == "PASS", f"Status should be 'PASS', but got '{data['status']}'."