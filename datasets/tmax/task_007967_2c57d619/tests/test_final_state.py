# test_final_state.py

import os
import ctypes
import re

def test_rust_project_files_exist():
    """Verify that the Rust project files and Cargo.toml exist."""
    cargo_toml_path = "/home/user/rust_lib/Cargo.toml"
    assert os.path.exists(cargo_toml_path), f"{cargo_toml_path} does not exist"

    with open(cargo_toml_path, "r") as f:
        content = f.read()

    # Check for cdylib and name
    assert re.search(r'crate-type\s*=\s*\[\s*["\']cdylib["\']\s*\]', content), "Cargo.toml must specify crate-type = ['cdylib']"
    assert re.search(r'name\s*=\s*["\']proxy_abi["\']', content), "Cargo.toml must specify name = 'proxy_abi'"

def test_shared_library_exists():
    """Verify that the compiled shared library exists."""
    so_path = "/home/user/rust_lib/target/debug/libproxy_abi.so"
    assert os.path.exists(so_path), f"Compiled library {so_path} does not exist. Did you run `cargo build`?"

def test_python_script_exists():
    """Verify that the Python test script exists."""
    py_path = "/home/user/test_proxy.py"
    assert os.path.exists(py_path), f"Python script {py_path} does not exist."

def test_result_log_content():
    """Verify the content of the result.log file."""
    log_path = "/home/user/result.log"
    assert os.path.exists(log_path), f"Result log {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "http://backend_service:9090", f"Expected 'http://backend_service:9090', got '{content}'"

def test_rust_library_functionality():
    """Load the shared library and test the extract_target function directly."""
    so_path = "/home/user/rust_lib/target/debug/libproxy_abi.so"
    if not os.path.exists(so_path):
        pytest.skip("Shared library not found, skipping functionality test.")

    lib = ctypes.CDLL(so_path)
    assert hasattr(lib, "extract_target"), "extract_target function is not exported by the library."

    lib.extract_target.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_size_t]
    lib.extract_target.restype = ctypes.c_int32

    # Test valid payload
    # route_type (1 byte) = 0x01
    # path_len (2 bytes) = 7
    # path = /api/v3
    # target_len (2 bytes) = 27
    # target = http://backend_service:9090
    valid_payload = b'\x01\x00\x07/api/v3\x00\x1bhttp://backend_service:9090'
    out_buf = ctypes.create_string_buffer(100)

    res = lib.extract_target(valid_payload, len(valid_payload), out_buf, 100)
    assert res == 27, f"Expected return value 27, got {res}"
    assert out_buf.value == b"http://backend_service:9090", f"Expected output buffer to contain target, got {out_buf.value}"

    # Test invalid route type
    invalid_route = b'\x02\x00\x07/api/v3\x00\x1bhttp://backend_service:9090'
    out_buf2 = ctypes.create_string_buffer(100)
    res2 = lib.extract_target(invalid_route, len(invalid_route), out_buf2, 100)
    assert res2 == -1, f"Expected -1 for invalid route type, got {res2}"

    # Test invalid path
    invalid_path = b'\x01\x00\x07/api/v4\x00\x1bhttp://backend_service:9090'
    out_buf3 = ctypes.create_string_buffer(100)
    res3 = lib.extract_target(invalid_path, len(invalid_path), out_buf3, 100)
    assert res3 == -1, f"Expected -1 for invalid path, got {res3}"