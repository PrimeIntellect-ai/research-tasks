# test_final_state.py

import os
import subprocess
import ctypes
import pytest

BASE_DIR = "/home/user/polyglot_system"

def test_test_results_log():
    log_path = os.path.join(BASE_DIR, "test_results.log")
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "PROPERTY_TESTS_PASSED" in content, f"Expected 'PROPERTY_TESTS_PASSED' in {log_path}, found {content!r}"

def test_rust_code_fixed():
    lib_rs_path = os.path.join(BASE_DIR, "rust_encoder/src/lib.rs")
    assert os.path.isfile(lib_rs_path), f"Rust source {lib_rs_path} is missing."

    with open(lib_rs_path, "r") as f:
        content = f.read()

    assert "no_mangle" in content, "Rust code is missing #[no_mangle] attribute."
    assert "extern \"C\"" in content, "Rust code is missing extern \"C\"."

def test_build_artifacts_exist():
    so_path = os.path.join(BASE_DIR, "lib/librust_encoder.so")
    bin_path = os.path.join(BASE_DIR, "bin/go_encoder")

    assert os.path.isfile(so_path), f"Rust shared object {so_path} is missing."
    assert os.path.isfile(bin_path), f"Go executable {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"Go executable {bin_path} is not executable."

def test_go_encoder_execution():
    bin_path = os.path.join(BASE_DIR, "bin/go_encoder")
    assert os.path.isfile(bin_path), "Go executable not found."

    test_str = "hello"
    expected_hex = test_str.encode('utf-8').hex()

    try:
        result = subprocess.run([bin_path, test_str], capture_output=True, text=True, timeout=2)
        assert result.returncode == 0, f"Go executable failed with return code {result.returncode}"

        # The go code might output characters out of order if they are not sorted properly, 
        # but wait, the prompt says the go code processes characters and appends them. 
        # Actually, the original go code uses a channel and appends as they come in, 
        # which means the order is non-deterministic. However, the prompt says "fix the deadlock".
        # Let's just verify it returns a hex string of the correct length and doesn't deadlock.
        out = result.stdout.strip()
        assert len(out) == len(expected_hex), "Go executable output length mismatch."
    except subprocess.TimeoutExpired:
        pytest.fail("Go executable timed out, indicating a deadlock is still present.")

def test_rust_library_execution():
    so_path = os.path.join(BASE_DIR, "lib/librust_encoder.so")
    assert os.path.isfile(so_path), "Rust shared object not found."

    try:
        lib = ctypes.CDLL(so_path)
    except OSError as e:
        pytest.fail(f"Failed to load Rust shared object: {e}")

    assert hasattr(lib, "encode_hex"), "encode_hex function not found in shared object. Was #[no_mangle] used?"

    encode_hex = lib.encode_hex
    encode_hex.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    encode_hex.restype = None

    input_str = b"test string"
    expected_hex = input_str.hex().encode('utf-8')
    output_buf = ctypes.create_string_buffer(512)

    encode_hex(input_str, output_buf)

    assert output_buf.value == expected_hex, f"Rust encode_hex produced incorrect output: {output_buf.value} != {expected_hex}"

def test_build_script_exists():
    build_sh_path = os.path.join(BASE_DIR, "build.sh")
    assert os.path.isfile(build_sh_path), f"Build script {build_sh_path} is missing."

def test_verify_script_exists():
    verify_py_path = os.path.join(BASE_DIR, "verify.py")
    assert os.path.isfile(verify_py_path), f"Verification script {verify_py_path} is missing."