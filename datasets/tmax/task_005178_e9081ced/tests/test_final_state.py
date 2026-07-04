# test_final_state.py
import os
import subprocess
import pytest
import tempfile
import math

def test_bad_commit_txt():
    bad_commit_file = "/home/user/bad_commit.txt"
    expected_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(bad_commit_file), f"{bad_commit_file} does not exist."
    assert os.path.isfile(expected_file), f"Truth file {expected_file} is missing."

    with open(bad_commit_file, "r") as f:
        actual_commit = f.read().strip()

    with open(expected_file, "r") as f:
        expected_commit = f.read().strip()

    assert actual_commit == expected_commit, f"Expected bad commit {expected_commit}, but got {actual_commit}"

def test_make_success():
    repo_path = "/home/user/trajectory_calc"
    result = subprocess.run(["make"], cwd=repo_path, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with output:\n{result.stderr}\n{result.stdout}"
    assert os.path.isfile(os.path.join(repo_path, "trajectory.o")), "trajectory.o was not built."

def test_calc_y_logic():
    repo_path = "/home/user/trajectory_calc"
    test_c_content = """
#include <stdio.h>
#include "trajectory.h"

int main() {
    double y = calc_y(10.0, 2.0);
    printf("%f\\n", y);
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_c_path = os.path.join(tmpdir, "test_calc.c")
        test_bin_path = os.path.join(tmpdir, "test_calc")
        with open(test_c_path, "w") as f:
            f.write(test_c_content)

        compile_res = subprocess.run(
            ["gcc", test_c_path, os.path.join(repo_path, "trajectory.o"), "-I" + repo_path, "-o", test_bin_path],
            capture_output=True, text=True
        )
        assert compile_res.returncode == 0, f"Failed to compile test program against trajectory.o:\n{compile_res.stderr}"

        run_res = subprocess.run([test_bin_path], capture_output=True, text=True)
        assert run_res.returncode == 0, "Test program crashed."

        try:
            val = float(run_res.stdout.strip())
        except ValueError:
            pytest.fail(f"Output was not a float: {run_res.stdout}")

        assert math.isclose(val, 0.4, rel_tol=1e-5), f"calc_y(10.0, 2.0) should be 0.4, but got {val}"

def test_fuzzer_exists_and_runs():
    fuzzer_path = "/home/user/trajectory_calc/fuzzer"
    assert os.path.isfile(fuzzer_path), f"Fuzzer executable not found at {fuzzer_path}"
    assert os.access(fuzzer_path, os.X_OK), f"Fuzzer at {fuzzer_path} is not executable."

    result = subprocess.run([fuzzer_path, "-runs=1"], capture_output=True, text=True)
    assert result.returncode == 0, f"Fuzzer failed to run successfully:\n{result.stderr}\n{result.stdout}"
    assert "Done" in result.stderr or "stat::" in result.stderr, "Output does not look like a successful libFuzzer run."