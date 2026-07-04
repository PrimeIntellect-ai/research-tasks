# test_final_state.py
import os
import stat
import subprocess

def test_minimal_crash_txt():
    filepath = "/home/user/uptime_monitor/minimal_crash.txt"
    assert os.path.isfile(filepath), f"{filepath} does not exist."

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"minimal_crash.txt should contain exactly 3 lines, found {len(lines)}."

    content = " ".join(lines)
    assert "AuthService DBService" in content or "DBService AuthService" in content, "Missing AuthService/DBService link."
    assert "DBService CacheService" in content or "CacheService DBService" in content, "Missing DBService/CacheService link."
    assert "CacheService AuthService" in content or "AuthService CacheService" in content, "Missing CacheService/AuthService link."

def test_regression_script_and_execution():
    script_path = "/home/user/uptime_monitor/regression_test.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"{script_path} is not executable."

    # Run the script
    result = subprocess.run([script_path], cwd="/home/user/uptime_monitor", capture_output=True, text=True)
    assert result.returncode == 0, f"regression_test.sh failed with exit code {result.returncode}. stderr: {result.stderr}"

    # Check test_result.log
    log_path = "/home/user/uptime_monitor/test_result.log"
    assert os.path.isfile(log_path), f"{log_path} was not created."

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "CYCLE DETECTED" in log_content, "test_result.log does not contain 'CYCLE DETECTED'."