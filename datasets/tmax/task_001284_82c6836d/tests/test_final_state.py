# test_final_state.py
import os
import json
import stat
import pytest

def test_rca_json():
    rca_path = "/home/user/rca.json"
    assert os.path.isfile(rca_path), f"File not found: {rca_path}"

    with open(rca_path, "r") as f:
        try:
            rca_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{rca_path} is not valid JSON")

    assert rca_data.get("bug_function") == "process_metric", "Incorrect 'bug_function' in rca.json"
    assert rca_data.get("first_anomaly_timestamp") == "2024-05-10T03:14:22", "Incorrect 'first_anomaly_timestamp' in rca.json"
    assert rca_data.get("failed_metric_id") == 105, "Incorrect 'failed_metric_id' in rca.json"

def test_server_fixed_c():
    fixed_c_path = "/home/user/app/server_fixed.c"
    assert os.path.isfile(fixed_c_path), f"File not found: {fixed_c_path}"

    with open(fixed_c_path, "r") as f:
        content = f.read()

    # Check if the missing unlock was added to the error block
    # We look for the error block and see if unlock is present before returning.
    # The original had:
    # if (!converged) {
    #     printf("ERROR: Convergence failure for metric %d\n", metric_id);
    #     // BUG: Missed unlock on error path
    #     return;
    # }

    # We can check if `pthread_mutex_unlock` appears multiple times in process_metric
    # Or simply check if it exists in the fixed file between the error print and the return.

    # A simple and robust check: The file must contain the unlock statement.
    assert "pthread_mutex_unlock" in content, "Missing pthread_mutex_unlock in server_fixed.c"

    # Let's count the occurrences of pthread_mutex_unlock in process_metric
    # It should be at least 2 now (one for success, one for error).
    # Since process_metric is the only function using it, counting overall is fine.
    unlock_count = content.count("pthread_mutex_unlock(&state_mutex);")
    assert unlock_count >= 2, "Expected at least 2 pthread_mutex_unlock calls in server_fixed.c to fix the deadlock"

def test_server_fixed_executable():
    executable_path = "/home/user/app/server_fixed"
    assert os.path.isfile(executable_path), f"Executable not found: {executable_path}"

    # Check if it's executable
    st = os.stat(executable_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File is not executable: {executable_path}"