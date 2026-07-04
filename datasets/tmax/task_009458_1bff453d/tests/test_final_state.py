# test_final_state.py

import os
import subprocess
import pytest

def test_cimonitor_amd64_exists_and_arch():
    binary_path = "/home/user/cimonitor_amd64"
    assert os.path.isfile(binary_path), f"{binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

    result = subprocess.run(["file", binary_path], capture_output=True, text=True)
    assert result.returncode == 0, f"file command failed on {binary_path}"
    assert "ELF 64-bit" in result.stdout and ("x86-64" in result.stdout or "AMD64" in result.stdout.upper()), \
        f"{binary_path} is not an x86-64 executable. file output: {result.stdout}"

def test_cimonitor_arm64_exists_and_arch():
    binary_path = "/home/user/cimonitor_arm64"
    assert os.path.isfile(binary_path), f"{binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

    result = subprocess.run(["file", binary_path], capture_output=True, text=True)
    assert result.returncode == 0, f"file command failed on {binary_path}"
    assert "ELF 64-bit" in result.stdout and ("aarch64" in result.stdout or "ARM aarch64" in result.stdout), \
        f"{binary_path} is not an ARM64 executable. file output: {result.stdout}"

def test_build_summary_log():
    log_path = "/home/user/build_summary.log"
    assert os.path.isfile(log_path), f"{log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "/home/user/cimonitor_amd64" in content, "build_summary.log missing amd64 binary info."
    assert "/home/user/cimonitor_arm64" in content, "build_summary.log missing arm64 binary info."
    assert "ELF 64-bit" in content, "build_summary.log does not contain expected 'file' output."

def test_fixes_patch():
    patch_path = "/home/user/fixes.patch"
    assert os.path.isfile(patch_path), f"{patch_path} is missing."

    with open(patch_path, "r") as f:
        content = f.read()

    assert "diff --git" in content or "--- " in content, f"{patch_path} does not look like a valid patch file."

def test_go_build_succeeds():
    workdir = "/home/user/cimonitor"
    assert os.path.isdir(workdir), f"{workdir} directory is missing."

    result = subprocess.run(["go", "build"], cwd=workdir, capture_output=True, text=True)
    assert result.returncode == 0, f"go build failed in {workdir}. Output:\n{result.stderr}\n{result.stdout}"

def test_cimonitor_runs_without_deadlock():
    binary_path = "/home/user/cimonitor_amd64"
    assert os.path.isfile(binary_path), f"{binary_path} is missing."

    try:
        result = subprocess.run([binary_path], capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        pytest.fail("cimonitor deadlocked (timed out after 5 seconds).")

    assert result.returncode == 0, f"cimonitor failed to run. Output:\n{result.stderr}\n{result.stdout}"
    assert "Processed: state-helper_val: pipeline started" in result.stdout, \
        f"cimonitor output missing expected processed lines. Output:\n{result.stdout}"