# test_final_state.py
import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/backend_feature"
VALGRIND_REPORT = "/home/user/valgrind_report.txt"

def test_valgrind_report_exists_and_contains_leak():
    assert os.path.isfile(VALGRIND_REPORT), f"Valgrind report missing at {VALGRIND_REPORT}"
    with open(VALGRIND_REPORT, "r") as f:
        content = f.read().lower()
    assert "valgrind" in content, "The file does not appear to be a valgrind report."
    assert "definitely lost:" in content, "Valgrind report does not seem to indicate the initial memory leak ('definitely lost:')."

def test_binaries_exist():
    native_bin = os.path.join(WORKSPACE_DIR, "processor_native")
    web_bin = os.path.join(WORKSPACE_DIR, "processor_web")
    assert os.path.isfile(native_bin), f"Compiled binary missing: {native_bin}"
    assert os.path.isfile(web_bin), f"Compiled binary missing: {web_bin}"
    assert os.access(native_bin, os.X_OK), f"Binary {native_bin} is not executable."
    assert os.access(web_bin, os.X_OK), f"Binary {web_bin} is not executable."

def test_native_binary_output():
    native_bin = os.path.join(WORKSPACE_DIR, "processor_native")
    result = subprocess.run([native_bin], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {native_bin} failed."
    output = result.stdout.strip()
    assert "Mode: Native" in output, f"processor_native output incorrect. Expected 'Mode: Native', got:\n{output}"
    assert "Processed: GET / HTTP/1.1" in output, f"processor_native output missing 'Processed: GET / HTTP/1.1', got:\n{output}"

def test_web_binary_output():
    web_bin = os.path.join(WORKSPACE_DIR, "processor_web")
    result = subprocess.run([web_bin], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {web_bin} failed."
    output = result.stdout.strip()
    assert "Mode: Web" in output, f"processor_web output incorrect. Expected 'Mode: Web', got:\n{output}"
    assert "Processed: GET / HTTP/1.1" in output, f"processor_web output missing 'Processed: GET / HTTP/1.1', got:\n{output}"

def test_memory_leak_fixed():
    native_bin = os.path.join(WORKSPACE_DIR, "processor_native")
    result = subprocess.run(
        ["valgrind", "--leak-check=full", native_bin],
        capture_output=True,
        text=True
    )
    stderr_output = result.stderr
    assert "definitely lost: 0 bytes in 0 blocks" in stderr_output, \
        "Memory leak not fixed. Valgrind output does not show '0 bytes in 0 blocks' definitely lost."