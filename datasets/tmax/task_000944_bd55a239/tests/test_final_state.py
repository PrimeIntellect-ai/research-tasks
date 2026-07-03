# test_final_state.py
import os
import subprocess
import ctypes

def test_project_directory_exists():
    assert os.path.isdir('/home/user/project'), "Directory /home/user/project/ does not exist."

def test_build_and_test_script_execution():
    script_path = '/home/user/project/build_and_test.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Execute the script
    result = subprocess.run(
        [script_path],
        cwd='/home/user/project',
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"build_and_test.sh failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_library_and_log_exist():
    # These should exist after the script runs
    so_path = '/home/user/project/libbloom.so'
    log_path = '/home/user/project/result.log'

    assert os.path.isfile(so_path), f"Shared library {so_path} does not exist after running build_and_test.sh."
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist after running build_and_test.sh."

    with open(log_path, 'r') as f:
        content = f.read().strip()
    assert content == "SUCCESS: ALL PROPERTIES PASSED", f"Unexpected content in result.log: {content}"

def test_bloom_filter_abi_and_logic():
    so_path = '/home/user/project/libbloom.so'
    assert os.path.isfile(so_path), f"Shared library {so_path} is missing."

    try:
        lib = ctypes.CDLL(so_path)
    except OSError as e:
        assert False, f"Failed to load shared library: {e}"

    # Setup ABI
    try:
        lib.bloom_create.argtypes = [ctypes.c_int, ctypes.c_double]
        lib.bloom_create.restype = ctypes.c_void_p

        lib.bloom_add.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.bloom_add.restype = None

        lib.bloom_check.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.bloom_check.restype = ctypes.c_int

        lib.bloom_destroy.argtypes = [ctypes.c_void_p]
        lib.bloom_destroy.restype = None
    except AttributeError as e:
        assert False, f"Library is missing required ABI function: {e}"

    # Test logic
    bloom = lib.bloom_create(1000, 0.01)
    assert bloom is not None, "bloom_create returned NULL pointer."

    try:
        lib.bloom_add(bloom, b"test_string_1")
        lib.bloom_add(bloom, b"test_string_2")

        assert lib.bloom_check(bloom, b"test_string_1") == 1, "False negative on test_string_1"
        assert lib.bloom_check(bloom, b"test_string_2") == 1, "False negative on test_string_2"
        assert lib.bloom_check(bloom, b"test_string_3") == 0, "False positive on empty filter for test_string_3 (or extremely unlucky collision)"
    finally:
        lib.bloom_destroy(bloom)