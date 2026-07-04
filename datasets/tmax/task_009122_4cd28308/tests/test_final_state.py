# test_final_state.py
import os

def test_flag_file_exists_and_correct():
    """Test that the flag file was created and contains the correct flag."""
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"Flag file {flag_path} does not exist. Did you run the script and save the output?"

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{jwt_n0n3_byp4ss_m4st3r}"
    assert content == expected_flag, f"Flag file content is incorrect. Expected '{expected_flag}', but found '{content}'."

def test_audit_log_redacted():
    """Test that the audit log was properly redacted and saved to the correct location."""
    redacted_log_path = "/home/user/audit_redacted.log"
    assert os.path.isfile(redacted_log_path), f"Redacted log file {redacted_log_path} does not exist."

    with open(redacted_log_path, "r") as f:
        lines = f.read().splitlines()

    expected_lines = [
        "[INFO] User login: [REDACTED] from 192.168.1.10",
        "[WARN] Failed login for [REDACTED]",
        "[INFO] Data exported by [REDACTED] successfully.",
        "[DEBUG] No emails here just some text."
    ]

    assert len(lines) == len(expected_lines), f"Redacted log has {len(lines)} lines, but expected {len(expected_lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in redacted log is incorrect.\nExpected: '{expected}'\nGot: '{actual}'"