# test_final_state.py

import os
import json
import pytest

REPORT_PATH = '/home/user/report.json'
PLOT_PATH = '/home/user/vibration_hist.png'

def test_report_exists_and_valid_json():
    """Check that report.json exists and is valid JSON."""
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"
    try:
        with open(REPORT_PATH, 'r') as f:
            json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {REPORT_PATH} is not valid JSON.")

def test_report_contents():
    """Check the computed values in the report.json."""
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    # Check cleaned_rows
    assert "cleaned_rows" in data, "Key 'cleaned_rows' missing from report.json"
    assert data["cleaned_rows"] == 8, f"Expected 8 cleaned rows, got {data['cleaned_rows']}"

    # Check t_stat
    assert "t_stat" in data, "Key 't_stat' missing from report.json"
    t_stat = data["t_stat"]
    assert isinstance(t_stat, (int, float)), "t_stat must be a number"
    assert -0.101 <= t_stat <= -0.099, f"t_stat {t_stat} is not within the expected range (-0.101 to -0.099)"

    # Check ci_lower
    assert "ci_lower" in data, "Key 'ci_lower' missing from report.json"
    ci_lower = data["ci_lower"]
    assert isinstance(ci_lower, (int, float)), "ci_lower must be a number"
    assert 4.69 <= ci_lower <= 4.70, f"ci_lower {ci_lower} is not within the expected range (4.69 to 4.70)"

    # Check ci_upper
    assert "ci_upper" in data, "Key 'ci_upper' missing from report.json"
    ci_upper = data["ci_upper"]
    assert isinstance(ci_upper, (int, float)), "ci_upper must be a number"
    assert 5.27 <= ci_upper <= 5.29, f"ci_upper {ci_upper} is not within the expected range (5.27 to 5.29)"

def test_plot_exists_and_not_empty():
    """Check that the plot was generated and is not empty."""
    assert os.path.isfile(PLOT_PATH), f"Plot file not found at {PLOT_PATH}"
    assert os.path.getsize(PLOT_PATH) > 0, f"Plot file {PLOT_PATH} is empty (0 bytes)."