# test_final_state.py
import os

def test_audit_violations_log_exists():
    """Check if the audit_violations.log file was created."""
    assert os.path.exists("/home/user/audit_violations.log"), "The file /home/user/audit_violations.log is missing."

def test_audit_violations_log_contents():
    """Verify the contents of audit_violations.log are exact and sorted."""
    with open("/home/user/audit_violations.log", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "VIOLATION: AppServer1 connects to InternalAPI_A connects to UserDB",
        "VIOLATION: WebFront connects to InternalAPI_D connects to FinancialDB"
    ]

    assert lines == expected_lines, (
        f"Contents of /home/user/audit_violations.log do not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Found: {lines}"
    )

def test_c_program_exists():
    """Check if auditor.c and the compiled executable exist."""
    assert os.path.exists("/home/user/auditor.c"), "/home/user/auditor.c is missing."
    assert os.path.exists("/home/user/auditor"), "Compiled executable /home/user/auditor is missing."
    assert os.access("/home/user/auditor", os.X_OK), "/home/user/auditor is not executable."

def test_python_script_exists():
    """Check if query_runner.py exists."""
    assert os.path.exists("/home/user/query_runner.py"), "/home/user/query_runner.py is missing."

def test_system_graph_exists():
    """Check if system_graph.ttl exists."""
    assert os.path.exists("/home/user/system_graph.ttl"), "/home/user/system_graph.ttl is missing."