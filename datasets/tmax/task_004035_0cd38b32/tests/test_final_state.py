# test_final_state.py

import os
import subprocess
import pytest

def test_directory_structure():
    """Verify that the source files have been reorganized correctly."""
    base_dir = "/home/user/stack-vm"

    assert os.path.isfile(os.path.join(base_dir, "include", "vm_engine.h")), "include/vm_engine.h is missing."
    assert os.path.isfile(os.path.join(base_dir, "src", "vm_engine.cpp")), "src/vm_engine.cpp is missing."
    assert os.path.isfile(os.path.join(base_dir, "src", "main.cpp")), "src/main.cpp is missing."

    # Check that they are no longer in the root directory
    assert not os.path.exists(os.path.join(base_dir, "vm_engine.h")), "vm_engine.h should be moved to include/"
    assert not os.path.exists(os.path.join(base_dir, "vm_engine.cpp")), "vm_engine.cpp should be moved to src/"
    assert not os.path.exists(os.path.join(base_dir, "main.cpp")), "main.cpp should be moved to src/"

def test_build_outputs():
    """Verify that the CMake configuration correctly built the targets in the specified directories."""
    base_dir = "/home/user/stack-vm"
    bin_path = os.path.join(base_dir, "build", "bin", "vm-cli")
    lib_path = os.path.join(base_dir, "build", "lib", "libvm_engine.so")

    assert os.path.isfile(bin_path), f"Executable not found at {bin_path}. Check CMake output directories."
    assert os.path.isfile(lib_path), f"Shared library not found at {lib_path}. Check CMake output directories."

def test_executable_rpath():
    """Verify that the executable runs without LD_LIBRARY_PATH, implying correct RPATH."""
    base_dir = "/home/user/stack-vm"
    bin_path = os.path.join(base_dir, "build", "bin", "vm-cli")

    # Run the executable with no arguments. It should return 1 and print usage, but not fail with shared library error.
    # We clear LD_LIBRARY_PATH to ensure it relies on RPATH.
    env = os.environ.copy()
    env.pop("LD_LIBRARY_PATH", None)

    try:
        result = subprocess.run([bin_path], env=env, capture_output=True, text=True)
        # Usage error returns 1, missing shared library usually returns 127
        assert result.returncode == 1, f"Expected return code 1 (usage error), got {result.returncode}. Output: {result.stderr}"
        assert "Usage:" in result.stderr, f"Executable failed to run properly. Missing shared library? Error: {result.stderr}"
    except FileNotFoundError:
        pytest.fail(f"Executable {bin_path} not found.")

def test_result_log():
    """Verify that the final output log contains the correct result."""
    log_path = "/home/user/result.log"

    assert os.path.isfile(log_path), f"Result log not found at {log_path}. Did you run the emulator with prog2.txt?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "25", f"Expected result log to contain '25', but got '{content}'."