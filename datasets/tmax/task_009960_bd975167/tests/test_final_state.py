# test_final_state.py
import os

def test_flag_file_exists_and_correct():
    """Test that flag.txt exists and contains the correct flag."""
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"File {flag_path} does not exist. The script might not have run correctly or didn't write the output."

    with open(flag_path, 'r') as f:
        flag_content = f.read().strip()

    expected_flag = "FLAG{crYpt0_l0gg3r_byp4ss_772}"
    assert flag_content == expected_flag, f"The flag in {flag_path} is incorrect. Expected '{expected_flag}', got '{flag_content}'."

def test_exploit_c_exists():
    """Test that the exploit C program was created."""
    exploit_path = "/home/user/exploit.c"
    assert os.path.isfile(exploit_path), f"The exploit source file {exploit_path} is missing."

def test_parse_log_py_exists():
    """Test that the log parsing Python script was created."""
    parser_path = "/home/user/parse_log.py"
    assert os.path.isfile(parser_path), f"The Python script {parser_path} is missing."

def test_audit_log_contains_success():
    """Test that the audit log contains the successful exploit entry."""
    audit_log_path = "/home/user/vuln_logger/audit.log"
    assert os.path.isfile(audit_log_path), f"The audit log file {audit_log_path} is missing. The logger daemon may not have run."

    with open(audit_log_path, 'r') as f:
        audit_content = f.read()

    assert "EXPLOIT_SUCCESS" in audit_content, "The audit log does not contain the expected 'EXPLOIT_SUCCESS' message."
    assert "FLAG{crYpt0_l0gg3r_byp4ss_772}" in audit_content, "The audit log does not contain the flag, indicating the payload was likely invalid."
    assert "AUTH: ADMIN" in audit_content, "The audit log does not show an ADMIN authentication, indicating the exploit didn't use the ADMIN token."