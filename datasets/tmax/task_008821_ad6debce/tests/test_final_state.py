# test_final_state.py
import os
import subprocess

def test_bad_commit_txt():
    expected_path = "/tmp/expected_bad_commit.txt"
    user_path = "/home/user/bad_commit.txt"

    assert os.path.isfile(expected_path), "Expected bad commit file missing."
    assert os.path.isfile(user_path), "User bad commit file missing."

    with open(expected_path, "r") as f:
        expected_commit = f.read().strip()

    with open(user_path, "r") as f:
        user_commit = f.read().strip()

    assert expected_commit == user_commit, f"Incorrect bad commit. Expected {expected_commit}, got {user_commit}."

def test_crash_func_txt():
    user_path = "/home/user/crash_func.txt"
    assert os.path.isfile(user_path), "User crash func file missing."

    with open(user_path, "r") as f:
        func_name = f.read().strip()

    valid_funcs = ["unsafe_cleanup", "trigger_payload", "clear"]
    assert any(valid in func_name for valid in valid_funcs), f"Incorrect crash function. Got {func_name}."

def test_patch_and_compile():
    repo_path = "/home/user/suspicious_daemon"
    service_cpp = os.path.join(repo_path, "service.cpp")
    service_bin = os.path.join(repo_path, "service")

    assert os.path.isfile(service_cpp), f"Source file {service_cpp} missing."

    # Compile the code
    compile_result = subprocess.run(
        ["g++", "-pthread", "service.cpp", "-o", "service"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert compile_result.returncode == 0, f"Compilation failed: {compile_result.stderr}"
    assert os.path.isfile(service_bin), "Compiled binary not found."

    # Run the binary 100 times to ensure it doesn't crash
    for i in range(100):
        run_result = subprocess.run(
            ["./service"],
            cwd=repo_path,
            capture_output=True
        )
        assert run_result.returncode == 0, f"Binary crashed on run {i+1}."