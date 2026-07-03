# test_final_state.py

import os
import subprocess
import pytest

def test_makefile_fixed():
    makefile_path = "/home/user/project/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing."

    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-g" in content, "Makefile does not include debugging symbols (-g)."

    # Check if make succeeds
    result = subprocess.run(["make", "-C", "/home/user/project", "clean", "all"], capture_output=True)
    assert result.returncode == 0, f"make failed:\n{result.stderr.decode()}"

    executable = "/home/user/project/artifact_filter"
    assert os.path.isfile(executable), "artifact_filter executable was not created."
    assert os.access(executable, os.X_OK), "artifact_filter is not executable."

def test_c_code_fixed():
    c_file = "/home/user/project/artifact_filter.c"
    assert os.path.isfile(c_file), "artifact_filter.c is missing."

    with open(c_file, "r") as f:
        content = f.read()
    assert "free(" in content, "artifact_filter.c does not contain a call to free()."

    # Ensure it's compiled before running valgrind
    subprocess.run(["make", "-C", "/home/user/project", "all"], capture_output=True)

    executable = "/home/user/project/artifact_filter"
    # Run valgrind
    valgrind_cmd = [
        "valgrind",
        "--leak-check=full",
        "--error-exitcode=255",
        executable,
        "100"
    ]

    result = subprocess.run(valgrind_cmd, input=b"size: 50\n", capture_output=True)
    # Valgrind returns 255 if there is a leak/error, otherwise it returns the program's exit code (0 here)
    assert result.returncode != 255, f"Valgrind detected memory leaks or errors:\n{result.stderr.decode()}"

def test_ci_pipeline_script():
    script_path = "/home/user/ci_pipeline.sh"
    assert os.path.isfile(script_path), "ci_pipeline.sh is missing."
    assert os.access(script_path, os.X_OK), "ci_pipeline.sh is not executable."

    with open(script_path, "r") as f:
        content = f.read()
    assert "sleep 0.5" in content or "sleep .5" in content, "ci_pipeline.sh does not contain the rate limit sleep (sleep 0.5)."

def test_approved_log():
    log_path = "/home/user/approved.log"
    assert os.path.isfile(log_path), "approved.log is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = ["art1.txt", "art3.txt"]
    assert lines == expected, f"approved.log content is incorrect. Expected {expected}, got {lines}."