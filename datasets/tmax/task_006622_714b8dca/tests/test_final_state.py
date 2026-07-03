# test_final_state.py
import os
import subprocess

def test_status_file():
    status_path = "/home/user/stats_engine/status.txt"
    assert os.path.isfile(status_path), "status.txt is missing"
    with open(status_path, "r") as f:
        content = f.read().strip()
    assert content == "SUCCESS", f"Expected 'SUCCESS' in status.txt, got '{content}'"

def test_make_test_succeeds():
    # This verifies the Makefile is fixed (e.g., -lm added) and stats.c logic is fixed
    result = subprocess.run(
        ["make", "test"],
        cwd="/home/user/stats_engine",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'make test' failed with output:\n{result.stdout}\n{result.stderr}"

def test_minimized_test_exists_and_compiles():
    minimized_test_path = "/home/user/stats_engine/minimized_test.c"
    assert os.path.isfile(minimized_test_path), "minimized_test.c is missing"

    compile_result = subprocess.run(
        ["gcc", "-I./src", "-o", "minimized_test", "minimized_test.c", "src/stats.c", "-lm"],
        cwd="/home/user/stats_engine",
        capture_output=True,
        text=True
    )
    assert compile_result.returncode == 0, f"Compilation of minimized_test.c failed:\n{compile_result.stderr}"

def test_minimized_test_execution():
    executable_path = "/home/user/stats_engine/minimized_test"
    assert os.path.isfile(executable_path), "minimized_test executable is missing, compile step might have failed"

    run_result = subprocess.run(
        [executable_path],
        cwd="/home/user/stats_engine",
        capture_output=True,
        text=True
    )
    assert run_result.returncode == 0, f"minimized_test execution failed (returned {run_result.returncode}). Output:\n{run_result.stdout}\n{run_result.stderr}"