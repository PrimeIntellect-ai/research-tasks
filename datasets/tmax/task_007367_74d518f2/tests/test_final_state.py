# test_final_state.py
import os
import subprocess
import ctypes
import pytest

def test_libwaf_so_exists_and_is_elf():
    lib_path = "/home/user/project/ext/libwaf.so"
    assert os.path.exists(lib_path), f"{lib_path} does not exist."
    with open(lib_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"{lib_path} is not a valid ELF file."

def test_waf_c_vulnerability_fixed():
    waf_c_path = "/home/user/project/ext/waf.c"
    assert os.path.exists(waf_c_path), f"{waf_c_path} does not exist."
    with open(waf_c_path, "r") as f:
        content = f.read()
    assert "i <= len" not in content, "The OOB read vulnerability (i <= len) was not fixed in waf.c."

def test_waf_c_contains_check_sqli_c():
    waf_c_path = "/home/user/project/ext/waf.c"
    assert os.path.exists(waf_c_path), f"{waf_c_path} does not exist."
    with open(waf_c_path, "r") as f:
        content = f.read()
    assert "check_sqli_c" in content, "check_sqli_c function is missing from waf.c."

def test_unittest_passes():
    test_dir = "/home/user/project"
    result = subprocess.run(
        ["python3", "-m", "unittest", "tests.test_waf"],
        cwd=test_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Unittests failed:\n{result.stdout}\n{result.stderr}"

def test_benchmark_log_exists_and_correct():
    log_path = "/home/user/project/bench_results.log"
    assert os.path.exists(log_path), f"{log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()

    assert "PYTHON_TIME:" in content, "PYTHON_TIME missing from benchmark log."
    assert "C_TIME:" in content, "C_TIME missing from benchmark log."
    assert "C_IS_FASTER: True" in content, "C_IS_FASTER: True missing from benchmark log."

def test_check_sqli_c_functionality():
    lib_path = "/home/user/project/ext/libwaf.so"
    if not os.path.exists(lib_path):
        pytest.skip("libwaf.so not found, skipping functionality test.")

    lib = ctypes.CDLL(lib_path)

    assert hasattr(lib, "check_sqli_c"), "check_sqli_c not exported in libwaf.so"
    lib.check_sqli_c.argtypes = [ctypes.c_char_p]
    lib.check_sqli_c.restype = ctypes.c_int

    payload1 = b"admin' OR 1=1 -- UNION SELECT * FROM users"
    payload2 = b"hello world"

    assert lib.check_sqli_c(payload1) == 1, "check_sqli_c failed to detect SQLi in a malicious payload."
    assert lib.check_sqli_c(payload2) == 0, "check_sqli_c falsely detected SQLi in a benign payload."