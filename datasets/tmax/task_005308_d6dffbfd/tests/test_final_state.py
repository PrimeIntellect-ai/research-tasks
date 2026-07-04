# test_final_state.py

import os
import subprocess
import pytest

def test_vproc_bin_compiled_and_linked():
    bin_path = "/home/user/deploy/bin/vproc_bin"
    assert os.path.isfile(bin_path), f"Binary not found: {bin_path}"
    assert os.access(bin_path, os.X_OK), f"Binary is not executable: {bin_path}"

    try:
        ldd_output = subprocess.check_output(["ldd", bin_path], text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run ldd on {bin_path}: {e}")

    assert "libcustom_filter.so" in ldd_output, "vproc_bin is not dynamically linked to libcustom_filter.so"
    assert "not found" not in ldd_output, "vproc_bin has missing dynamic libraries (rpath might be missing)"

def test_video_result():
    result_path = "/home/user/deploy/video_result.txt"
    assert os.path.isfile(result_path), f"Video result file not found: {result_path}"

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "27", f"Expected video result to be '27', but got '{content}'"

def test_run_integration_exists():
    script_path = "/home/user/run_integration.sh"
    assert os.path.isfile(script_path), f"Integration test script not found: {script_path}"

def test_validate_routes_adversarial_corpus():
    script_path = "/home/user/deploy/validate_routes.sh"
    assert os.path.isfile(script_path), f"Validator script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Validator script is not executable: {script_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for fpath in clean_files:
        res = subprocess.run([script_path, fpath], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(fpath))

    evil_bypassed = []
    for fpath in evil_files:
        res = subprocess.run([script_path, fpath], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(fpath))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean files rejected (expected exit code 0): {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil files bypassed (expected exit code 1): {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail("Adversarial corpus validation failed:\n" + "\n".join(errors))