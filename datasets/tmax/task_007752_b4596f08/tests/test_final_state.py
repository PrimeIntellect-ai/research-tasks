# test_final_state.py

import os
import subprocess
import tempfile
import hashlib

RUNNER_PATH = "/home/user/ci_runner.sh"
PB_PATH = "/home/user/project/main.pb"
ENV_FILE = "/home/user/build_env.sh"
LOG_FILE = "/home/user/build_output.log"

def test_runner_exists_and_executable():
    assert os.path.isfile(RUNNER_PATH), f"Script {RUNNER_PATH} does not exist."
    assert os.access(RUNNER_PATH, os.X_OK), f"Script {RUNNER_PATH} is not executable."

def test_runner_success_path():
    assert os.path.isfile(PB_PATH), f"Test setup file {PB_PATH} is missing."

    result = subprocess.run([RUNNER_PATH, PB_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}. Stderr: {result.stderr}\nStdout: {result.stdout}"

    assert os.path.isfile(ENV_FILE), f"{ENV_FILE} was not created."
    with open(ENV_FILE, "r") as f:
        env_content = f.read()

    assert "export THRESHOLD=24" in env_content, f"{ENV_FILE} missing 'export THRESHOLD=24'. Content:\n{env_content}"
    assert "export WORKERS=4" in env_content, f"{ENV_FILE} missing 'export WORKERS=4'. Content:\n{env_content}"

    assert os.path.isfile(LOG_FILE), f"{LOG_FILE} was not created."
    with open(LOG_FILE, "r") as f:
        log_content = f.read().strip()

    assert "[SUCCESS] CI Pipeline Passed" in log_content, f"Log file missing success message. Content:\n{log_content}"

def test_runner_checksum_failure():
    with tempfile.TemporaryDirectory() as tmpdir:
        dummy_file = os.path.join(tmpdir, "dummy.txt")
        with open(dummy_file, "w") as f:
            f.write("test data")

        pb_path = os.path.join(tmpdir, "fail.pb")
        with open(pb_path, "w") as f:
            f.write("CHECKSUM dummy.txt invalidhash123\n")

        result = subprocess.run([RUNNER_PATH, pb_path], capture_output=True, text=True)
        assert result.returncode == 1, f"Expected exit code 1 for checksum failure, got {result.returncode}"

        assert os.path.isfile(LOG_FILE), f"{LOG_FILE} was not created during checksum failure."
        with open(LOG_FILE, "r") as f:
            log_content = f.read().strip()
        assert "[ERROR] Checksum failed for dummy.txt" in log_content, f"Missing checksum error in log. Content:\n{log_content}"

def test_runner_build_failure():
    with tempfile.TemporaryDirectory() as tmpdir:
        pb_path = os.path.join(tmpdir, "fail_build.pb")
        with open(pb_path, "w") as f:
            f.write("BUILD exit 1\n")

        result = subprocess.run([RUNNER_PATH, pb_path], capture_output=True, text=True)
        assert result.returncode == 2, f"Expected exit code 2 for build failure, got {result.returncode}"

        assert os.path.isfile(LOG_FILE), f"{LOG_FILE} was not created during build failure."
        with open(LOG_FILE, "r") as f:
            log_content = f.read().strip()
        assert "[ERROR] Build failed: exit 1" in log_content, f"Missing build error in log. Content:\n{log_content}"

def test_runner_clears_log_and_env():
    # Write garbage to files
    with open(ENV_FILE, "w") as f:
        f.write("GARBAGE_ENV\n")
    with open(LOG_FILE, "w") as f:
        f.write("GARBAGE_LOG\n")

    with tempfile.TemporaryDirectory() as tmpdir:
        pb_path = os.path.join(tmpdir, "empty.pb")
        with open(pb_path, "w") as f:
            f.write("")

        subprocess.run([RUNNER_PATH, pb_path], capture_output=True, text=True)

        with open(ENV_FILE, "r") as f:
            env_content = f.read()
        assert "GARBAGE_ENV" not in env_content, f"{ENV_FILE} was not cleared before execution."

        with open(LOG_FILE, "r") as f:
            log_content = f.read()
        assert "GARBAGE_LOG" not in log_content, f"{LOG_FILE} was not cleared before execution."