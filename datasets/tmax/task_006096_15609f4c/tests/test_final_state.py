# test_final_state.py

import os
import subprocess
import pytest

def test_final_output_log():
    log_path = "/home/user/migration/final_output.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, 'r') as f:
        content = f.read().strip()
    assert content == "noitargim", f"Expected 'noitargim' in {log_path}, but got '{content}'"

def test_rust_so_exists():
    so_path = "/home/user/migration/rust_ext/target/release/librust_ext.so"
    assert os.path.isfile(so_path), f"Rust shared library {so_path} does not exist. Did you run cargo build --release?"

def test_app_py_migrated():
    app_path = "/home/user/migration/app.py"
    assert os.path.isfile(app_path), f"Python 3 app file {app_path} does not exist."
    with open(app_path, 'r') as f:
        content = f.read()
    assert "BaseHTTPServer" not in content, "BaseHTTPServer is still in app.py, so it was not properly migrated to Python 3."
    assert "ctypes" in content, "ctypes not found in app.py. FFI integration is missing."

def test_nginx_running():
    conf_path = "/home/user/migration/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config {conf_path} does not exist."

    # Check if nginx is running with this config
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    assert "nginx" in result.stdout and conf_path in result.stdout, "Nginx does not appear to be running with the specified config."

def test_python_app_running():
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    assert "app.py" in result.stdout and "python" in result.stdout.lower(), "app.py does not appear to be running in the background."

def test_pytest_file_passes():
    test_file = "/home/user/migration/test_app.py"
    assert os.path.isfile(test_file), f"Pytest file {test_file} does not exist."

    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest {test_file} failed. Output:\n{result.stdout}\n{result.stderr}"

def test_rust_lib_rs_fixed():
    lib_rs = "/home/user/migration/rust_ext/src/lib.rs"
    assert os.path.isfile(lib_rs), f"Rust source file {lib_rs} does not exist."
    with open(lib_rs, 'r') as f:
        content = f.read()
    assert "into_raw" in content, "The Rust code does not seem to use into_raw() to prevent the dangling pointer."