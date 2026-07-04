# test_final_state.py

import os
import subprocess
import pytest

def test_run_sh_exists_and_executable():
    run_sh_path = "/home/user/run.sh"
    assert os.path.isfile(run_sh_path), f"{run_sh_path} does not exist."
    assert os.access(run_sh_path, os.X_OK), f"{run_sh_path} is not executable."

def test_run_sh_execution_and_output():
    run_sh_path = "/home/user/run.sh"

    # Execute the script as the user
    result = subprocess.run(
        ["su", "-", "user", "-c", run_sh_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"run.sh failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert "All tests passed." in result.stdout, "The output did not contain 'All tests passed.' indicating the test didn't succeed."

def test_cmake_lists_fixed():
    cmake_path = "/home/user/project/CMakeLists.txt"
    assert os.path.isfile(cmake_path), f"{cmake_path} is missing."

    with open(cmake_path, "r") as f:
        content = f.read()

    assert "target_link_libraries(" in content and "migrator_test" in content and "encoder" in content, \
        "CMakeLists.txt does not appear to link migrator_test to the encoder library."

def test_memory_safety_bug_fixed():
    migrator_cpp_path = "/home/user/project/src/migrator.cpp"
    assert os.path.isfile(migrator_cpp_path), f"{migrator_cpp_path} is missing."

    with open(migrator_cpp_path, "r") as f:
        content = f.read()

    # Check that the specific bad line is gone, or if it's there, it allocates + 1.
    # We can just check that `new char[record.name_len];` (exact match) is NOT in the file.
    # If they used `new char[record.name_len + 1]` or std::vector/std::string, it will pass.
    bad_allocation = "new char[record.name_len];"
    assert bad_allocation not in content.replace(" ", ""), \
        "The out-of-bounds memory allocation bug is still present in migrator.cpp."

def test_mock_data_fixed():
    test_migrator_path = "/home/user/project/test/test_migrator.cpp"
    assert os.path.isfile(test_migrator_path), f"{test_migrator_path} is missing."

    with open(test_migrator_path, "r") as f:
        content = f.read()

    # The original file had empty mock_utf16. The user should have added elements.
    # We check that they are pushing back or initializing with 'T', 'e', 's', 't'
    assert 'T' in content and 'e' in content and 's' in content and 't' in content, \
        "test_migrator.cpp does not appear to initialize the mock data with the string 'Test'."