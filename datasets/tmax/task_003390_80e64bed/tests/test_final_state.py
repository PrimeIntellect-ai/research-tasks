# test_final_state.py
import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_makefile_builds_successfully():
    """Test that running make successfully builds libdataparser.so and app."""
    # Run make clean if it exists, but we don't strictly require it.
    subprocess.run(["make", "clean"], cwd=PROJECT_DIR, capture_output=True)

    result = subprocess.run(["make"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Make failed with output:\n{result.stderr}\n{result.stdout}"

    # Check if the expected files are built
    assert os.path.isfile(os.path.join(PROJECT_DIR, "libdataparser.so")), "libdataparser.so was not built."
    assert os.path.isfile(os.path.join(PROJECT_DIR, "app")), "app executable was not built."

def test_main_c_memory_leak_fixed():
    """Test that main.c calls free_parsed_data."""
    main_c_path = os.path.join(PROJECT_DIR, "main.c")
    with open(main_c_path, "r") as f:
        content = f.read()

    assert "free_parsed_data(" in content, "main.c does not seem to call free_parsed_data to fix the memory leak."

def test_run_tests_script_exists_and_executable():
    """Test that run_tests.sh exists and is executable."""
    script_path = os.path.join(PROJECT_DIR, "run_tests.sh")
    assert os.path.isfile(script_path), "run_tests.sh script is missing."
    assert os.access(script_path, os.X_OK), "run_tests.sh script is not executable."

def test_run_tests_script_behavior():
    """Test the behavior of run_tests.sh with valgrind and output redirection."""
    script_path = os.path.join(PROJECT_DIR, "run_tests.sh")
    output_log_path = os.path.join(PROJECT_DIR, "output.log")

    # Remove output.log if it exists to ensure it's generated
    if os.path.exists(output_log_path):
        os.remove(output_log_path)

    payload = "role:admin,id:404"
    result = subprocess.run([script_path, payload], cwd=PROJECT_DIR, capture_output=True, text=True)

    assert result.returncode == 0, f"run_tests.sh failed (possibly due to memory leaks). stderr:\n{result.stderr}\nstdout:\n{result.stdout}"

    assert os.path.isfile(output_log_path), "output.log was not created by run_tests.sh."

    with open(output_log_path, "r") as f:
        log_content = f.read().strip()

    expected_output = "Key: role | Value: admin\nKey: id | Value: 404"
    assert log_content == expected_output, f"output.log does not contain the expected output. Got:\n{log_content}"

def test_run_tests_script_contents():
    """Test that run_tests.sh contains valgrind and required flags."""
    script_path = os.path.join(PROJECT_DIR, "run_tests.sh")
    with open(script_path, "r") as f:
        content = f.read()

    assert "valgrind" in content, "run_tests.sh does not use valgrind."
    assert "--leak-check=full" in content, "run_tests.sh does not use --leak-check=full."
    assert "--error-exitcode=1" in content, "run_tests.sh does not use --error-exitcode=1."
    assert "output.log" in content, "run_tests.sh does not redirect to output.log."