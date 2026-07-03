# test_final_state.py

import os
import subprocess
import pytest

SERVICE_DIR = "/home/user/forensic_service"

def test_compilation_succeeds():
    """Verify that the project successfully compiles after fixing the interface mismatch."""
    res = subprocess.run(
        ["go", "build", "./..."],
        cwd=SERVICE_DIR,
        capture_output=True,
        text=True
    )
    assert res.returncode == 0, f"Project fails to compile. Output:\n{res.stderr}"

def test_tests_pass():
    """Verify that all tests, including the newly added regression test, pass."""
    res = subprocess.run(
        ["go", "test", "./..."],
        cwd=SERVICE_DIR,
        capture_output=True,
        text=True
    )
    assert res.returncode == 0, f"Tests fail. Output:\n{res.stdout}\n{res.stderr}"

def test_db_go_modifications():
    """Verify that db.go has been fixed correctly."""
    db_path = os.path.join(SERVICE_DIR, "db", "db.go")
    assert os.path.exists(db_path), f"{db_path} does not exist."

    with open(db_path, "r") as f:
        db_content = f.read()

    assert "[]*models.Event" not in db_content, "Interface signature mismatch (returning pointers) not fixed properly in db.go."
    assert "[]models.Event" in db_content, "GetCriticalEvents should return []models.Event."
    assert "&ev.Action, &ev.Username" not in db_content, "Row scanning bug (swapped Action and Username) not fixed in db.go."

def test_db_test_go_exists_and_content():
    """Verify that db_test.go exists and contains the required regression test."""
    test_file = os.path.join(SERVICE_DIR, "db", "db_test.go")
    assert os.path.exists(test_file), f"{test_file} does not exist."

    with open(test_file, "r") as f:
        test_content = f.read()

    assert "TestGetCriticalEvents" in test_content, "TestGetCriticalEvents function missing in db_test.go."
    assert "UNAUTHORIZED_ACCESS" in test_content, "Test does not contain required test data (UNAUTHORIZED_ACCESS)."
    assert "bob" in test_content, "Test does not contain required test data (bob)."
    assert "alice" in test_content, "Test does not contain required test data (alice)."
    assert "eve" in test_content, "Test does not contain required test data (eve)."

def test_fix_report_log():
    """Verify that the fix report log is created with the exact correct format."""
    log_file = os.path.join(SERVICE_DIR, "fix_report.log")
    assert os.path.exists(log_file), f"{log_file} does not exist."

    with open(log_file, "r") as f:
        log_content = f.read()

    assert "STATUS: FIXED" in log_content, "fix_report.log missing 'STATUS: FIXED'."
    assert "TEST_PASSED: TRUE" in log_content, "fix_report.log missing 'TEST_PASSED: TRUE'."
    assert "COMPILER_ISSUE_ROOT_CAUSE:" in log_content, "fix_report.log missing 'COMPILER_ISSUE_ROOT_CAUSE:'."
    assert "QUERY_ISSUE_ROOT_CAUSE:" in log_content, "fix_report.log missing 'QUERY_ISSUE_ROOT_CAUSE:'."