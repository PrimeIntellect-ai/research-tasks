# test_final_state.py
import os
import re

def test_venv_exists():
    venv_path = "/home/user/project/venv"
    assert os.path.isdir(venv_path), f"Virtual environment directory {venv_path} does not exist. Did you create it?"

def test_makefile_fixed():
    makefile_path = "/home/user/project/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} is missing."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-shared" in content, "Makefile does not contain the '-shared' flag for gcc."
    assert "-fPIC" in content, "Makefile does not contain the '-fPIC' flag for gcc."

def test_db_py_fixed():
    db_py_path = "/home/user/project/db.py"
    assert os.path.isfile(db_py_path), f"{db_py_path} is missing."
    with open(db_py_path, "r") as f:
        content = f.read()
    # Check if user_id was replaced with account_id in the SELECT query
    assert "SELECT account_id" in content, "db.py was not updated to select 'account_id' instead of 'user_id'."
    assert "SELECT user_id" not in content, "db.py still contains 'SELECT user_id', which is the old schema."

def test_ci_results_log():
    log_path = "/home/user/ci_results.log"
    assert os.path.isfile(log_path), f"CI results log {log_path} does not exist. Did you run the CI script?"
    with open(log_path, "r") as f:
        content = f.read()
    assert "1 passed" in content, f"{log_path} does not indicate a successful test run ('1 passed' not found)."