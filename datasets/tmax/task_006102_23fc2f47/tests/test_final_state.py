# test_final_state.py
import os
import json
import math

def test_stability_report_json():
    json_path = "/home/user/stability_report.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not a valid JSON file."

    assert "mse_rk45" in data, "Key 'mse_rk45' missing in stability_report.json"
    assert "mse_bdf" in data, "Key 'mse_bdf' missing in stability_report.json"

    assert isinstance(data["mse_rk45"], (int, float)), "'mse_rk45' must be a float"
    assert isinstance(data["mse_bdf"], (int, float)), "'mse_bdf' must be a float"

    assert data["mse_rk45"] > 0, "'mse_rk45' must be greater than 0"
    assert data["mse_bdf"] > 0, "'mse_bdf' must be greater than 0"

def test_training_data_csv():
    csv_path = "/home/user/training_data.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 101, f"Expected 101 lines in {csv_path}, found {len(lines)}"
    assert lines[0] == "t,y1,y2", f"Expected header 't,y1,y2', found '{lines[0]}'"

    # Calculate truth
    for i in range(100):
        t = i / 99.0
        y1 = (998/999) * math.exp(-1000 * t) + (1/999) * math.exp(-t)
        y2 = math.exp(-t)

        expected_line = f"{round(t, 6):.6f},{round(y1, 6):.6f},{round(y2, 6):.6f}"
        # pandas round might strip trailing zeros, so let's parse floats to compare
        actual_parts = lines[i+1].split(',')
        assert len(actual_parts) == 3, f"Line {i+2} does not have 3 columns"

        actual_t, actual_y1, actual_y2 = map(float, actual_parts)

        assert math.isclose(actual_t, round(t, 6), rel_tol=1e-6, abs_tol=1e-6), \
            f"Row {i+1}: expected t={round(t, 6)}, got {actual_t}"
        assert math.isclose(actual_y1, round(y1, 6), rel_tol=1e-6, abs_tol=1e-6), \
            f"Row {i+1}: expected y1={round(y1, 6)}, got {actual_y1}"
        assert math.isclose(actual_y2, round(y2, 6), rel_tol=1e-6, abs_tol=1e-6), \
            f"Row {i+1}: expected y2={round(y2, 6)}, got {actual_y2}"