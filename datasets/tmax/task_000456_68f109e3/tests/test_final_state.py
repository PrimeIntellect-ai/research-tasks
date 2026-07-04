# test_final_state.py
import os
import stat
import subprocess
import tarfile
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_ci_script():
    script_path = "/home/user/account_system/ci_run.sh"
    if not os.path.exists(script_path):
        pytest.fail(f"Required script {script_path} does not exist.")
    if not os.access(script_path, os.X_OK):
        pytest.fail(f"Script {script_path} is not executable.")

    # Clean up previous state to ensure supervisor restart logic and pipeline are tested cleanly
    cleanup_files = [
        "/home/user/account_system/db.lock",
        "/home/user/account_system/fail_state.tmp",
        "/home/user/account_system/ci_status.log",
        "/home/user/account_system/release.tar.gz",
        "/home/user/account_system/profiles/groupA/user1.json",
        "/home/user/account_system/profiles/user2.json"
    ]
    for f in cleanup_files:
        if os.path.exists(f):
            os.remove(f)

    # Execute the pipeline script
    subprocess.run([script_path], cwd="/home/user/account_system", capture_output=True, text=True)

def test_ci_run_exists_and_executable():
    script_path = "/home/user/account_system/ci_run.sh"
    assert os.path.exists(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_supervisor_execution_success():
    # If supervisor logic is correct, it should wait for db_init, then run profile_gen,
    # handle the first failure, restart it, and eventually succeed, creating the profile.
    profile_path = "/home/user/account_system/profiles/groupA/user1.json"
    assert os.path.exists(profile_path), (
        "Supervisor did not successfully run profile_gen.py to completion. "
        "Check dependency waiting and restart policies."
    )

def test_ci_status_log():
    log_path = "/home/user/account_system/ci_status.log"
    assert os.path.exists(log_path), f"Log file {log_path} was not created."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "SUCCESS", f"Expected ci_status.log to contain exactly 'SUCCESS', got '{content}'."

def test_release_tarball_exists_and_valid():
    tar_path = "/home/user/account_system/release.tar.gz"
    assert os.path.exists(tar_path), f"Tarball {tar_path} was not created."
    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar archive."

    with tarfile.open(tar_path, "r:gz") as tar:
        names = tar.getnames()
        # Ensure it contains the expected files
        assert any("user1.json" in name for name in names), "Tarball does not contain the generated profiles."

def test_profile_permissions():
    profiles_dir = "/home/user/account_system/profiles"
    assert os.path.exists(profiles_dir), f"Directory {profiles_dir} does not exist."

    for root, dirs, files in os.walk(profiles_dir):
        for d in dirs:
            dir_path = os.path.join(root, d)
            mode = stat.S_IMODE(os.stat(dir_path).st_mode)
            assert mode == 0o750, f"Directory {dir_path} has incorrect permissions: {oct(mode)} (expected 0o750)."

        for f in files:
            file_path = os.path.join(root, f)
            mode = stat.S_IMODE(os.stat(file_path).st_mode)
            assert mode == 0o640, f"File {file_path} has incorrect permissions: {oct(mode)} (expected 0o640)."