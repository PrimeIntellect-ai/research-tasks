# test_final_state.py
import os
import hashlib

def test_recovery_report_exists_and_correct():
    """Test that the recovery report exists and contains the correct findings."""
    report_path = "/home/user/forensics/recovery_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist. Did you create it?"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_pin = "82941"
    expected_flag = "CTF{m3m0ry_c0rrupt10n_f0r_th3_w1n}"
    expected_sha256 = hashlib.sha256(expected_flag.encode('utf-8')).hexdigest()

    expected_lines = {
        f"PIN: {expected_pin}",
        f"FLAG: {expected_flag}",
        f"FLAG_SHA256: {expected_sha256}"
    }

    found_lines = set(lines)

    for expected_line in expected_lines:
        assert expected_line in found_lines, f"Expected line '{expected_line}' not found in {report_path}."