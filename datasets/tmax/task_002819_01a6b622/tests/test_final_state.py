# test_final_state.py

import os
import re
import subprocess
import pytest

def test_libgsl_dev_installed():
    """Verify that libgsl-dev is installed."""
    try:
        result = subprocess.run(
            ["dpkg", "-s", "libgsl-dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        assert "Status: install ok installed" in result.stdout, "libgsl-dev is not fully installed."
    except subprocess.CalledProcessError:
        pytest.fail("libgsl-dev package is not installed.")

def test_regression_report_exists():
    """Verify that regression_report.log exists."""
    log_path = "/home/user/protein/regression_report.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

def test_regression_report_format_and_values():
    """Verify the format and contents of regression_report.log."""
    log_path = "/home/user/protein/regression_report.log"
    if not os.path.isfile(log_path):
        pytest.skip("Log file missing.")

    with open(log_path, "r") as f:
        content = f.read().strip()

    # Expected format:
    # Overall Mean: 8.169
    # 95% CI: [8.100, 8.200]
    # Regression: PASS

    lines = content.split('\n')
    assert len(lines) == 3, "Log file should contain exactly 3 lines."

    mean_match = re.match(r"^Overall Mean:\s*(\d+\.\d{3})$", lines[0])
    assert mean_match is not None, "Line 1 format is incorrect. Expected 'Overall Mean: <mean_rounded_to_3_decimals>'."

    overall_mean = float(mean_match.group(1))
    assert 7.969 <= overall_mean <= 8.369, f"Calculated overall mean {overall_mean} is not within 0.2 of 8.169."

    ci_match = re.match(r"^95% CI:\s*\[(\d+\.\d{3}),\s*(\d+\.\d{3})\]$", lines[1])
    assert ci_match is not None, "Line 2 format is incorrect. Expected '95% CI: [<lower_rounded_to_3_decimals>, <upper_rounded_to_3_decimals>]'."

    reg_match = re.match(r"^Regression:\s*(PASS|FAIL)$", lines[2])
    assert reg_match is not None, "Line 3 format is incorrect. Expected 'Regression: <PASS|FAIL>'."
    assert reg_match.group(1) == "PASS", "Regression test did not PASS as expected."