# test_final_state.py

import os
import re
import stat

def test_server_bin_exists_and_executable():
    bin_path = "/home/user/app/server_bin"
    assert os.path.exists(bin_path), f"Binary {bin_path} does not exist."
    assert os.path.isfile(bin_path), f"{bin_path} is not a file."

    st = os.stat(bin_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Binary {bin_path} is not executable."

def test_models_package_created():
    models_path = "/home/user/app/models/models.go"
    assert os.path.exists(models_path), f"File {models_path} does not exist."
    assert os.path.isfile(models_path), f"{models_path} is not a file."

    with open(models_path, "r") as f:
        content = f.read()

    assert "package models" in content, "models.go does not declare 'package models'."
    assert re.search(r"type\s+Request\s+struct", content), "models.go does not contain 'type Request struct'."

def test_limiter_test_exists():
    test_path = "/home/user/app/limiter/limiter_test.go"
    assert os.path.exists(test_path), f"Test file {test_path} does not exist."
    assert os.path.isfile(test_path), f"{test_path} is not a file."

def test_test_results_log():
    log_path = "/home/user/test_results.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    with open(log_path, "r") as f:
        content = f.read()

    assert "PASS" in content, "test_results.log does not contain 'PASS', tests might have failed."
    assert "TestLimiterConcurrent" in content, "test_results.log does not indicate TestLimiterConcurrent was run."