# test_final_state.py

import os
import subprocess

def test_build_script():
    """Verify build.sh exists, runs successfully, and creates libprocessor.so."""
    build_script = "/home/user/build.sh"
    so_file = "/home/user/libprocessor.so"

    assert os.path.isfile(build_script), f"{build_script} is missing."

    # Remove the .so file if it exists to ensure build.sh actually creates it
    if os.path.exists(so_file):
        os.remove(so_file)

    result = subprocess.run(["bash", build_script], capture_output=True, cwd="/home/user")
    assert result.returncode == 0, f"build.sh failed to execute. stderr: {result.stderr.decode()}"

    assert os.path.isfile(so_file), f"build.sh did not produce {so_file}."

def test_server_script_exists():
    """Verify server.py exists."""
    assert os.path.isfile("/home/user/server.py"), "/home/user/server.py is missing."

def test_test_server_script():
    """Verify test_server.py exists, passes pytest, and creates the correct log file."""
    test_script = "/home/user/test_server.py"
    log_file = "/home/user/test_result.log"

    assert os.path.isfile(test_script), f"{test_script} is missing."

    # Remove the log file if it exists to ensure the test creates it
    if os.path.exists(log_file):
        os.remove(log_file)

    result = subprocess.run(
        ["python3", "-m", "pytest", test_script],
        capture_output=True,
        cwd="/home/user"
    )
    assert result.returncode == 0, f"pytest on {test_script} failed.\nstdout: {result.stdout.decode()}\nstderr: {result.stderr.decode()}"

    assert os.path.isfile(log_file), f"{log_file} was not created by the test."

    with open(log_file, "r") as f:
        content = f.read().strip()

    assert content == "TEST PASSED", f"Expected 'TEST PASSED' in {log_file}, but got '{content}'."