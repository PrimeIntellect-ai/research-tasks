# test_final_state.py
import os
import stat
import subprocess
import pytest

def test_scripts_exist_and_executable():
    interpreter = "/home/user/interpreter.sh"
    run_tests = "/home/user/run_tests.sh"

    assert os.path.isfile(interpreter), f"{interpreter} does not exist."
    assert os.path.isfile(run_tests), f"{run_tests} does not exist."

    assert os.stat(interpreter).st_mode & stat.S_IXUSR, f"{interpreter} is not executable."
    assert os.stat(run_tests).st_mode & stat.S_IXUSR, f"{run_tests} is not executable."

def test_run_tests_and_verify_output():
    log_file = "/home/user/test_results.log"

    # Remove log file if it exists to ensure a fresh run
    if os.path.exists(log_file):
        os.remove(log_file)

    # Run the test harness script
    result = subprocess.run(
        ["/home/user/run_tests.sh"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"run_tests.sh failed with return code {result.returncode}.\nstdout: {result.stdout}\nstderr: {result.stderr}"

    assert os.path.isfile(log_file), f"Log file {log_file} was not created by run_tests.sh."

    with open(log_file, "r") as f:
        content = f.read().strip().splitlines()

    expected = ["15", "25", "35", "45", "55"]
    assert content == expected, f"Expected log contents {expected}, but got {content}."