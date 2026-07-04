# test_final_state.py
import os
import stat
import subprocess

def test_v2_db_exists_and_content():
    path = "/home/user/v2.db"
    assert os.path.exists(path), f"Missing {path}"
    with open(path, "r") as f:
        content = f.read().strip()

    expected_content = "1,admin,alice,true\n2,user,bob,true\n3,moderator,charlie,true"
    assert content == expected_content, f"Content of {path} is incorrect. Got:\n{content}"

def test_test_log_exists_and_content():
    path = "/home/user/test.log"
    assert os.path.exists(path), f"Missing {path}"
    with open(path, "r") as f:
        content = f.read().strip()

    expected_content = "Test suite passed: verified 3 entities.\nSUCCESS"
    assert content == expected_content, f"Content of {path} is incorrect. Got:\n{content}"

def test_orchestrate_script_exists_and_executable():
    path = "/home/user/orchestrate.sh"
    assert os.path.exists(path), f"Missing {path}"

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable"

def test_orchestrate_script_max_cores_constraint():
    path = "/home/user/orchestrate.sh"

    # Test with MAX_CORES=4 (should fail)
    env = os.environ.copy()
    env["MAX_CORES"] = "4"
    result = subprocess.run([path], env=env, capture_output=True)
    assert result.returncode == 1, "Script should exit with status 1 when MAX_CORES >= 4"

    # Test with MAX_CORES=5 (should fail)
    env["MAX_CORES"] = "5"
    result = subprocess.run([path], env=env, capture_output=True)
    assert result.returncode == 1, "Script should exit with status 1 when MAX_CORES >= 4"

def test_orchestrate_script_success_run():
    path = "/home/user/orchestrate.sh"

    # Remove artifacts to ensure the script recreates them correctly
    if os.path.exists("/home/user/v2.db"):
        os.remove("/home/user/v2.db")
    if os.path.exists("/home/user/test.log"):
        os.remove("/home/user/test.log")

    # Test with MAX_CORES=1 (should succeed)
    env = os.environ.copy()
    env["MAX_CORES"] = "1"
    result = subprocess.run([path], env=env, capture_output=True)
    assert result.returncode == 0, f"Script failed with MAX_CORES=1. Stderr: {result.stderr.decode()}"

    # Verify artifacts are recreated correctly
    assert os.path.exists("/home/user/v2.db"), "Script did not create /home/user/v2.db"
    assert os.path.exists("/home/user/test.log"), "Script did not create /home/user/test.log"

    with open("/home/user/test.log", "r") as f:
        content = f.read().strip()
    assert "SUCCESS" in content, "test.log did not contain SUCCESS after a successful run"