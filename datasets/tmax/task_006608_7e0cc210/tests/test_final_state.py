# test_final_state.py

import os
import subprocess
import pytest

def test_output_txt():
    output_path = "/home/user/project/output.txt"
    assert os.path.isfile(output_path), f"File {output_path} does not exist"

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "35", f"Expected output.txt to contain '35', but found '{content}'"

def test_libmath_exists():
    lib_path = "/home/user/project/lib/libmath.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist"

def test_app_exists():
    app_path = "/home/user/project/bin/app"
    assert os.path.isfile(app_path), f"Executable {app_path} does not exist"
    assert os.access(app_path, os.X_OK), f"File {app_path} is not executable"

def test_app_rpath_linking():
    app_path = "/home/user/project/bin/app"
    try:
        result = subprocess.run(["ldd", app_path], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running ldd on {app_path} failed: {e.stderr}")

    output = result.stdout
    # Check if libmath.so is resolved properly (should point to an absolute path containing project/lib/libmath.so)
    # e.g., libmath.so => /home/user/project/lib/libmath.so
    found = False
    for line in output.splitlines():
        if "libmath.so" in line and "=>" in line:
            parts = line.split("=>")
            if len(parts) == 2:
                resolved_path = parts[1].split()[0]
                if "project/lib/libmath.so" in resolved_path:
                    found = True
                    break

    assert found, "libmath.so is not properly linked with rpath or cannot be found by ldd"