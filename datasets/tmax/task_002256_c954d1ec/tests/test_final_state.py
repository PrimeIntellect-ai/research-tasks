# test_final_state.py
import json
import os
import math

def test_stability_report():
    report_path = "/home/user/stability_report.json"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {report_path} is not valid JSON."

    assert "slope_lu" in data, "Key 'slope_lu' missing from JSON."
    assert "slope_qr" in data, "Key 'slope_qr' missing from JSON."

    slope_lu = data["slope_lu"]
    slope_qr = data["slope_qr"]

    assert isinstance(slope_lu, (int, float)), "slope_lu must be a number."
    assert isinstance(slope_qr, (int, float)), "slope_qr must be a number."

    expected_lu = 0.9996
    expected_qr = 1.0028

    # 5% tolerance
    assert math.isclose(slope_lu, expected_lu, rel_tol=0.05), f"slope_lu {slope_lu} is not within 5% of {expected_lu}"
    assert math.isclose(slope_qr, expected_qr, rel_tol=0.05), f"slope_qr {slope_qr} is not within 5% of {expected_qr}"