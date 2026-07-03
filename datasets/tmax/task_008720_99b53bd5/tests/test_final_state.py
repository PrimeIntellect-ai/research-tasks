# test_final_state.py

import os
import subprocess
import re
import pytest

def test_bug_report():
    bug_report_path = "/home/user/bug_report.txt"
    assert os.path.exists(bug_report_path), f"File {bug_report_path} is missing."

    with open(bug_report_path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    expected_functions = {"check_health", "report_status"}
    assert set(lines) == expected_functions, f"bug_report.txt must contain exactly the two function names. Found: {lines}"

def test_mre_c():
    mre_path = "/home/user/mre.c"
    assert os.path.exists(mre_path), f"File {mre_path} is missing."

    with open(mre_path, "r") as f:
        content = f.read()

    for req in ["check_health", "report_status", "malloc", "free"]:
        assert req in content, f"mre.c must contain '{req}'"

    assert "pthread_mutex_lock" not in content, "mre.c must NOT contain 'pthread_mutex_lock'"

    # Check compilation
    compile_cmd = ["gcc", "-pthread", "-o", "/tmp/mre_bin", mre_path]
    result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"mre.c failed to compile:\n{result.stderr}"

def test_patched_c():
    patched_path = "/home/user/patched.c"
    assert os.path.exists(patched_path), f"File {patched_path} is missing."

    with open(patched_path, "r") as f:
        content = f.read()

    # Normalize whitespace for flexible matching
    normalized_content = re.sub(r'\s+', ' ', content)
    normalized_content_no_spaces = content.replace(" ", "").replace("\t", "").replace("\n", "")

    assert "pthread_mutex_t uptime_mutex" in normalized_content or "pthread_mutex_tuptime_mutex" in normalized_content_no_spaces, "patched.c must contain 'pthread_mutex_t uptime_mutex'"
    assert "pthread_mutex_lock(&uptime_mutex)" in normalized_content_no_spaces, "patched.c must contain 'pthread_mutex_lock(&uptime_mutex)'"
    assert "pthread_mutex_unlock(&uptime_mutex)" in normalized_content_no_spaces, "patched.c must contain 'pthread_mutex_unlock(&uptime_mutex)'"

    # Check compilation
    compile_cmd = ["gcc", "-pthread", "-o", "/tmp/patched_bin", patched_path]
    result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"patched.c failed to compile:\n{result.stderr}"

    # Run the compiled binary for 2 seconds
    try:
        run_result = subprocess.run(["/tmp/patched_bin"], timeout=2, capture_output=True)
        # If it exits before 2 seconds, check if it crashed
        assert run_result.returncode not in [134, 139], f"patched binary crashed with exit code {run_result.returncode}"
    except subprocess.TimeoutExpired:
        # Timeout is expected if it runs an infinite loop without crashing
        pass