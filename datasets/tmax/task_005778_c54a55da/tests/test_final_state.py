# test_final_state.py
import os
import time
import subprocess
import pytest

def test_watcher_functionality():
    cpp_file = "/home/user/config_watcher.cpp"
    executable = "/home/user/watcher"
    app_config = "/home/user/app_config.bin"
    symlink = "/home/user/active_env"
    log_file = "/home/user/watcher.log"

    assert os.path.isfile(cpp_file), f"Source code {cpp_file} not found."

    # Check if executable exists, if not, try to compile as the verification script does
    if not os.path.isfile(executable):
        compile_result = subprocess.run(
            ["g++", "-std=c++17", cpp_file, "-o", executable],
            capture_output=True,
            text=True
        )
        assert compile_result.returncode == 0, f"Compilation failed: {compile_result.stderr}"

    assert os.path.isfile(executable), f"Executable {executable} not found."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."
    assert os.path.isfile(app_config), f"Config file {app_config} not found."

    # Remove log file if it exists from previous runs
    if os.path.exists(log_file):
        os.remove(log_file)

    # Start the watcher
    process = subprocess.Popen([executable])
    try:
        # Give it time to initialize inotify
        time.sleep(1) 

        # Trigger 1
        with open(app_config, "r+b") as f:
            f.write(b"/home/user/env_v1".ljust(256, b"\0"))

        time.sleep(1)

        assert os.path.islink(symlink), f"Symlink {symlink} was not created after first modification."
        target1 = os.readlink(symlink)
        assert target1 == "/home/user/env_v1", f"Symlink points to wrong target: {target1}"

        # Trigger 2
        with open(app_config, "r+b") as f:
            f.write(b"/home/user/env_v2".ljust(256, b"\0"))

        time.sleep(1)

        assert os.path.islink(symlink), f"Symlink {symlink} is missing after second modification."
        target2 = os.readlink(symlink)
        assert target2 == "/home/user/env_v2", f"Symlink points to wrong target after update: {target2}"

    finally:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()

    assert os.path.isfile(log_file), f"Log file {log_file} was not created."
    with open(log_file, "r") as f:
        log_content = f.read()

    expected_log = "/home/user/env_v1\n/home/user/env_v2\n"
    assert log_content.strip() == expected_log.strip(), f"Log file content mismatch. Expected:\n{expected_log}\nGot:\n{log_content}"