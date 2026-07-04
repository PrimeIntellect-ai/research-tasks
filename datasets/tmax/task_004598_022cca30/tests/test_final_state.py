# test_final_state.py
import os
import subprocess
import filecmp

def test_audit_c_exists():
    path = "/home/user/audit.c"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_makefile_exists():
    path = "/home/user/Makefile"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_make_test():
    # Make sure we run make test in the correct directory
    work_dir = "/home/user"

    # Run make clean first to ensure a fresh build
    subprocess.run(["make", "clean"], cwd=work_dir, capture_output=True)

    # Run make test
    result = subprocess.run(["make", "test"], cwd=work_dir, capture_output=True, text=True)

    assert result.returncode == 0, f"'make test' failed with return code {result.returncode}. stderr: {result.stderr}"
    assert "CI Passed" in result.stdout, "'make test' output did not contain 'CI Passed'."

def test_audit_results_match():
    audit_results = "/home/user/audit_results.txt"
    expected_results = "/home/user/expected_results.txt"

    assert os.path.exists(audit_results), f"File {audit_results} was not created."

    with open(audit_results, 'r') as f1, open(expected_results, 'r') as f2:
        audit_content = f1.read()
        expected_content = f2.read()

    assert audit_content == expected_content, f"Contents of {audit_results} do not match {expected_results}."