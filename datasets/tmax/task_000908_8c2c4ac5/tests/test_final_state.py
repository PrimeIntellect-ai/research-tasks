# test_final_state.py
import os
import subprocess
import stat

def test_setup_script_exists_and_executable():
    path = "/home/user/setup_observability.sh"
    assert os.path.isfile(path), f"{path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_setup_script_execution_and_idempotency():
    setup_path = "/home/user/setup_observability.sh"

    # Run setup script
    result = subprocess.run([setup_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {setup_path} failed:\n{result.stderr}"

    # Check generated files
    assert os.path.isfile("/home/user/emitter"), "/home/user/emitter executable was not created."
    assert os.access("/home/user/emitter", os.X_OK), "/home/user/emitter is not executable."

    assert os.path.isdir("/home/user/dashboard_metrics"), "/home/user/dashboard_metrics directory was not created."

    wrapper_path = "/home/user/run_emitter.sh"
    assert os.path.isfile(wrapper_path), f"{wrapper_path} was not created."
    assert os.access(wrapper_path, os.X_OK), f"{wrapper_path} is not executable."

    # Check idempotency
    result2 = subprocess.run([setup_path], capture_output=True, text=True)
    assert result2.returncode == 0, f"Running {setup_path} a second time failed."

    with open(wrapper_path, "r") as f:
        lines = f.readlines()
    assert len(lines) < 20, f"{wrapper_path} grew too large, setup script is likely not idempotent."

def test_emitter_behavior_missing_env():
    # Ensure METRICS_OUT_DIR is unset
    env = os.environ.copy()
    env.pop("METRICS_OUT_DIR", None)

    result = subprocess.run(["/home/user/emitter"], env=env, capture_output=True, text=True)
    assert result.returncode != 0, "emitter should exit with a non-zero code when METRICS_OUT_DIR is missing."
    assert result.stderr.strip() != "", "emitter should print an error message to stderr when METRICS_OUT_DIR is missing."

def test_wrapper_script_behavior():
    wrapper_path = "/home/user/run_emitter.sh"
    log_path = "/home/user/dashboard_metrics/health.log"

    if os.path.exists(log_path):
        os.remove(log_path)

    result = subprocess.run([wrapper_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{wrapper_path} failed to execute properly."

    assert os.path.isfile(log_path), f"{log_path} was not created by the wrapper script."

    with open(log_path, "r") as f:
        content = f.read()

    assert "status=OK" in content, f"{log_path} does not contain 'status=OK'."