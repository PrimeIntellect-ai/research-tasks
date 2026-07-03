# test_final_state.py
import os
import subprocess
import re

def test_makefile_fixed():
    makefile_path = "/home/user/sensor_service/Makefile"
    assert os.path.exists(makefile_path), "Makefile is missing."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-fPIC" in content, "Makefile does not contain -fPIC flag, which is required to build shared libraries on x86 Linux."

def test_libsensor_built():
    so_path = "/home/user/sensor_service/libsensor.so"
    assert os.path.exists(so_path), "libsensor.so was not built. Ensure 'make' runs successfully."

def test_sensor_lib_c_fixes():
    c_path = "/home/user/sensor_service/sensor_lib.c"
    assert os.path.exists(c_path), "sensor_lib.c is missing."
    with open(c_path, "r") as f:
        content = f.read()

    # Check for usage of a 64-bit type to prevent overflow
    has_large_type = re.search(r'(size_t|uint64_t|int64_t|long\s+long)', content)
    assert has_large_type, "sensor_lib.c does not seem to use a 64-bit integer type (like size_t) to prevent the signed integer overflow."

    # Check for memory leak fix
    assert "free(" in content, "sensor_lib.c does not contain a 'free()' call to fix the memory leak."

def test_regression_log():
    log_path = "/home/user/sensor_service/regression_result.log"
    assert os.path.exists(log_path), "regression_result.log is missing. Did test_regression.py run and create it?"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "REGRESSION_TEST_PASSED", f"regression_result.log contains '{content}', expected exactly 'REGRESSION_TEST_PASSED'."

def test_regression_script_execution():
    script_path = "/home/user/sensor_service/test_regression.py"
    assert os.path.exists(script_path), "test_regression.py is missing."

    # Run the script to ensure it actually works and passes its own assertions
    result = subprocess.run(
        ["python3", script_path],
        cwd="/home/user/sensor_service",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"test_regression.py failed with exit code {result.returncode}.\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"