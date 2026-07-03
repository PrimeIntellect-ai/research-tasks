# test_final_state.py

import os
import re

def test_report_exists():
    """Verify that the report.txt file exists."""
    assert os.path.exists("/home/user/report.txt"), "/home/user/report.txt does not exist."
    assert os.path.isfile("/home/user/report.txt"), "/home/user/report.txt is not a file."

def test_report_content():
    """Verify the contents of report.txt."""
    with open("/home/user/report.txt", "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(lines) >= 3, "report.txt must contain at least 3 lines (Correlation, T-statistic, Top 3)."

    # Parse Correlation
    corr_match = re.search(r"Correlation:\s*([0-9\.\-]+)", content)
    assert corr_match is not None, "Could not find 'Correlation: [value]' in report.txt."
    corr_val = float(corr_match.group(1))
    assert abs(corr_val - 0.6953) <= 0.0002, f"Expected Correlation ~0.6953, got {corr_val}"

    # Parse T-statistic
    tstat_match = re.search(r"T-statistic:\s*([0-9\.\-]+)", content)
    assert tstat_match is not None, "Could not find 'T-statistic: [value]' in report.txt."
    tstat_val = float(tstat_match.group(1))
    assert abs(tstat_val - 6.7212) <= 0.0002, f"Expected T-statistic ~6.7212, got {tstat_val}"

    # Parse Top 3
    top3_match = re.search(r"Top 3:\s*(.*)", content)
    assert top3_match is not None, "Could not find 'Top 3: [IDs]' in report.txt."
    top3_val = top3_match.group(1).strip()
    expected_top3 = "COMP_2, COMP_42, COMP_33"
    assert top3_val == expected_top3, f"Expected Top 3: {expected_top3}, got {top3_val}"