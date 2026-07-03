# test_final_state.py
import os
import shutil
import subprocess
import pytest

def test_file_api_executable():
    path = "/home/user/file_api"
    assert os.path.isfile(path), f"File {path} does not exist"
    assert os.access(path, os.X_OK), f"File {path} is not executable"

def test_test_api_sh_executable():
    path = "/home/user/test_api.sh"
    assert os.path.isfile(path), f"File {path} does not exist"
    assert os.access(path, os.X_OK), f"File {path} is not executable"

def test_file_api_asan_and_deep_dir():
    asan_bin = "/tmp/file_api_asan"
    compile_cmd = [
        "g++", "-fsanitize=address", "-g", 
        "/home/user/file_api.cpp", "-o", asan_bin
    ]
    res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Compilation with ASAN failed:\n{res.stderr}"

    deep_dir = "/tmp/verify_dir"
    if os.path.exists(deep_dir):
        shutil.rmtree(deep_dir)

    current_dir = deep_dir
    os.makedirs(current_dir)
    # Create a deep structure with long names (>300 chars total)
    for _ in range(6):
        current_dir = os.path.join(current_dir, "a" * 60)
        os.makedirs(current_dir)

    env = os.environ.copy()
    env["QUERY_STRING"] = f"dir={deep_dir}"
    env["ASAN_OPTIONS"] = "detect_leaks=1:halt_on_error=1"

    res = subprocess.run([asan_bin], env=env, capture_output=True, text=True)
    assert res.returncode == 0, f"ASAN binary crashed or reported issues:\n{res.stderr}\n{res.stdout}"
    assert "AddressSanitizer" not in res.stderr, f"ASAN reported an error:\n{res.stderr}"

def test_test_api_sh_success():
    path = "/home/user/test_api.sh"
    res = subprocess.run([path], capture_output=True, text=True, cwd="/home/user")
    assert res.returncode == 0, f"{path} failed when it should succeed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"

def test_test_api_sh_failure():
    api_path = "/home/user/file_api"
    backup_path = "/home/user/file_api.bak"
    shutil.copy(api_path, backup_path)

    try:
        # Break the executable
        with open(api_path, "w") as f:
            f.write("#!/bin/bash\nexit 1\n")
        os.chmod(api_path, 0o755)

        test_path = "/home/user/test_api.sh"
        res = subprocess.run([test_path], capture_output=True, text=True, cwd="/home/user")
        assert res.returncode != 0, f"{test_path} should have failed when file_api is broken, but it exited with 0"
    finally:
        # Restore the original executable
        shutil.move(backup_path, api_path)