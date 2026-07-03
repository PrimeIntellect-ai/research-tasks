# test_final_state.py

import os
import stat
import subprocess
import pytest

def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def test_init_storage_sh():
    script_path = "/home/user/init_storage.sh"
    assert is_executable(script_path), f"{script_path} must exist and be executable."

    # Test idempotency and functionality
    # First, remove the directory if it exists to test creation
    subprocess.run(["rm", "-rf", "/home/user/app_data"])
    result = subprocess.run([script_path], capture_output=True)
    assert result.returncode == 0, f"{script_path} must exit with code 0."

    assert os.path.isdir("/home/user/app_data"), "/home/user/app_data must be created."
    quota_file = "/home/user/app_data/quota_config"
    assert os.path.isfile(quota_file), f"{quota_file} must be created."

    with open(quota_file, "r") as f:
        content = f.read().strip()
    assert content == "QUOTA=8192", f"{quota_file} must contain 'QUOTA=8192'."

    # Modify the file to test idempotency
    with open(quota_file, "w") as f:
        f.write("QUOTA=9999")

    result2 = subprocess.run([script_path], capture_output=True)
    assert result2.returncode == 0, f"{script_path} must exit with code 0 on second run."

    with open(quota_file, "r") as f:
        content2 = f.read().strip()
    assert content2 == "QUOTA=9999", f"{script_path} must not overwrite {quota_file} if it already exists."

    # Restore correct value
    with open(quota_file, "w") as f:
        f.write("QUOTA=8192")

def test_start_services_sh():
    script_path = "/home/user/start_services.sh"
    assert is_executable(script_path), f"{script_path} must exist and be executable."

def test_supervisor_c_fixes():
    c_file = "/home/user/supervisor.c"
    assert os.path.isfile(c_file), f"{c_file} must exist."

    with open(c_file, "r") as f:
        content = f.read()

    # Check for NULL check
    assert "NULL" in content or "!" in content, "supervisor.c must check if fopen returned NULL."
    # Check for parsing
    assert "sscanf" in content or "atoi" in content or "strtol" in content, "supervisor.c must parse the quota value."

def test_supervisor_compiled_and_safe():
    exe_path = "/home/user/supervisor"
    assert is_executable(exe_path), f"{exe_path} must be compiled and executable."

    # Test safe handling of missing file
    subprocess.run(["rm", "-rf", "/home/user/app_data/quota_config"])

    # Run supervisor, it should not segfault (return code 139)
    result = subprocess.run([exe_path], capture_output=True)
    assert result.returncode != 139, f"{exe_path} must not segfault when quota_config is missing."
    assert result.returncode != 0, f"{exe_path} should exit with non-zero status when config is missing."

    # Recreate config
    subprocess.run(["/home/user/init_storage.sh"])

def test_parse_metrics_sh():
    script_path = "/home/user/parse_metrics.sh"
    assert is_executable(script_path), f"{script_path} must exist and be executable."

def test_critical_sum_txt():
    sum_file = "/home/user/critical_sum.txt"
    assert os.path.isfile(sum_file), f"{sum_file} must exist."

    with open(sum_file, "r") as f:
        content = f.read().strip()

    assert content == "520", f"{sum_file} must contain the sum '520'."