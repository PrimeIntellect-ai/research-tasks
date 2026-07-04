# test_final_state.py

import os
import subprocess
import socket
import pytest

BASE_DIR = "/home/user/math_service"

def test_patch_applied():
    mathcore_path = os.path.join(BASE_DIR, "mathcore.c")
    assert os.path.isfile(mathcore_path), f"{mathcore_path} is missing."
    with open(mathcore_path, "r") as f:
        content = f.read()
    assert "compute_factors_adv" in content, "The feature patch was not applied to mathcore.c"
    assert "ADVANCED" in content, "The patch content is missing from mathcore.c"

def test_server_c_validation():
    server_path = os.path.join(BASE_DIR, "server.c")
    assert os.path.isfile(server_path), f"{server_path} is missing."
    with open(server_path, "r") as f:
        content = f.read()
    assert "ERR_NEGATIVE" in content, "server.c does not contain the required 'ERR_NEGATIVE' string for validation."
    assert "< 0" in content or "<0" in content, "server.c does not seem to check if n < 0."

def test_binaries_exist():
    lib_path = os.path.join(BASE_DIR, "libmathcore.so")
    bin_path = os.path.join(BASE_DIR, "math_server")
    assert os.path.isfile(lib_path), "libmathcore.so was not built or is missing."
    assert os.path.isfile(bin_path), "math_server was not built or is missing."

def test_rpath_configured():
    server_bin = os.path.join(BASE_DIR, "math_server")
    assert os.path.isfile(server_bin), "math_server binary is missing."
    try:
        output = subprocess.check_output(["readelf", "-d", server_bin], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run readelf on math_server: {e.output}")
    except FileNotFoundError:
        pytest.fail("readelf command not found. Cannot verify rpath.")

    has_rpath = False
    for line in output.splitlines():
        if "(RPATH)" in line or "(RUNPATH)" in line:
            if "ORIGIN" in line or BASE_DIR in line or "." in line:
                has_rpath = True
                break
    assert has_rpath, "math_server does not have correctly configured RPATH/RUNPATH pointing to the library location."

def test_test_results_log():
    log_path = os.path.join(BASE_DIR, "test_results.log")
    assert os.path.isfile(log_path), "test_results.log is missing."
    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "test_results.log does not contain at least 2 lines of output."
    assert lines[0] == "ERR_NEGATIVE", f"Expected first line to be 'ERR_NEGATIVE', got '{lines[0]}'."
    assert lines[1] == "ADVANCED:30", f"Expected second line to be 'ADVANCED:30', got '{lines[1]}'."

def test_server_running():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        result = s.connect_ex(("127.0.0.1", 8080))
        assert result == 0, "Server is not running or listening on 127.0.0.1:8080."
    finally:
        s.close()