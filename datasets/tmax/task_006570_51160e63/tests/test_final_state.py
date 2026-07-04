# test_final_state.py

import os
import subprocess
import pytest

def test_makefile_rpath():
    app_path = "/home/user/project/app"
    assert os.path.exists(app_path), "Executable 'app' not found at /home/user/project/app."

    result = subprocess.run(["readelf", "-d", app_path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run readelf on app."

    has_rpath = False
    for line in result.stdout.splitlines():
        if ("(RPATH)" in line or "(RUNPATH)" in line) and ("libs" in line or "/home/user/project/libs" in line):
            has_rpath = True
            break
    assert has_rpath, "The executable does not have the correct RPATH or RUNPATH set to point to the libs directory."

def test_app_c_memory_safety():
    app_c_path = "/home/user/project/app.c"
    assert os.path.exists(app_c_path), "app.c not found at /home/user/project/app.c."

    with open(app_c_path, "r") as f:
        content = f.read()

    assert "strcpy" not in content, "app.c still contains 'strcpy', which is unsafe and causes buffer overflow. You should use sscanf directly on the inputs."

def test_app_behavior():
    app_path = "/home/user/project/app"
    assert os.path.exists(app_path), "Executable 'app' not found."

    # We remove LD_LIBRARY_PATH to ensure rpath is actually working
    env = os.environ.copy()
    if "LD_LIBRARY_PATH" in env:
        del env["LD_LIBRARY_PATH"]

    result1 = subprocess.run([app_path, "2.1.5"], capture_output=True, text=True, env=env)
    assert result1.returncode == 0, f"Expected exit code 0 for version 2.1.5, got {result1.returncode}."

    result2 = subprocess.run([app_path, "1.9.0"], capture_output=True, text=True, env=env)
    assert result2.returncode == 1, f"Expected exit code 1 for version 1.9.0, got {result2.returncode}."

    result3 = subprocess.run([app_path, "10.20.30"], capture_output=True, text=True, env=env)
    assert result3.returncode == 0, f"Expected exit code 0 for version 10.20.30, got {result3.returncode}."

def test_test_py_exists_and_passes():
    test_py_path = "/home/user/project/test.py"
    assert os.path.exists(test_py_path), "test.py not found at /home/user/project/test.py."

    result = subprocess.run(["python3", test_py_path], capture_output=True, text=True, cwd="/home/user/project")
    assert result.returncode == 0, f"test.py failed to execute successfully. Output:\n{result.stderr}"
    assert "ALL TESTS PASSED" in result.stdout, "test.py did not print 'ALL TESTS PASSED' to stdout."

def test_success_log():
    log_path = "/home/user/project/success.log"
    assert os.path.exists(log_path), "success.log not found at /home/user/project/success.log."

    with open(log_path, "r") as f:
        content = f.read()

    assert "Beta library initialized." in content, "success.log is missing the 'Beta library initialized.' output."
    assert "Version OK: 2.1.5" in content, "success.log is missing the 'Version OK: 2.1.5' output."