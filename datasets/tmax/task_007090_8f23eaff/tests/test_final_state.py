# test_final_state.py

import os
import subprocess
import ctypes
import pytest

def test_librle_so_exists_and_valid():
    so_path = "/home/user/librle.so"
    assert os.path.isfile(so_path), f"{so_path} does not exist."

    # Try loading the shared library and accessing the function
    try:
        librle = ctypes.CDLL(so_path)
    except OSError as e:
        pytest.fail(f"Failed to load {so_path}: {e}")

    assert hasattr(librle, "rle_encode"), "Function 'rle_encode' not found in librle.so. Did you add extern \"C\"?"

    # Test bounds checking
    rle_encode = librle.rle_encode
    rle_encode.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    rle_encode.restype = None

    input_str = b"WWWWWWWWWWWWBWWWWWWWWWWWW"
    buf = ctypes.create_string_buffer(10)
    rle_encode(input_str, buf, 10)

    result = buf.value.decode('utf-8')
    assert len(result) < 10, "Result exceeds max_out_len."
    assert result.startswith("W9"), "Output encoding is incorrect."

def test_rle_patch_exists_and_valid():
    patch_path = "/home/user/rle.patch"
    assert os.path.isfile(patch_path), f"{patch_path} does not exist."

    with open(patch_path, 'r') as f:
        content = f.read()

    assert "---" in content and "+++" in content, "Patch does not appear to be a unified diff."
    assert "+" in content and "-" in content, "Patch does not contain added/removed lines."

def test_ffi_test_py_exists_and_runs():
    py_path = "/home/user/ffi_test.py"
    assert os.path.isfile(py_path), f"{py_path} does not exist."

    result = subprocess.run(["python3", py_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{py_path} failed to run. Stderr: {result.stderr}"

    output = result.stdout.strip()
    assert output.startswith("W9"), "Output from ffi_test.py is incorrect."
    assert len(output) < 10, "Output length from ffi_test.py exceeds buffer size."

def test_benchmark_sh_exists_and_runs():
    sh_path = "/home/user/benchmark.sh"
    log_path = "/home/user/benchmark.log"
    assert os.path.isfile(sh_path), f"{sh_path} does not exist."
    assert os.access(sh_path, os.X_OK), f"{sh_path} is not executable."

    if os.path.exists(log_path):
        initial_size = os.path.getsize(log_path)
    else:
        initial_size = 0

    result = subprocess.run(["bash", sh_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{sh_path} failed to run. Stderr: {result.stderr}"

    assert os.path.isfile(log_path), f"{log_path} was not created."
    new_size = os.path.getsize(log_path)
    assert new_size > initial_size, f"{log_path} was not appended to."