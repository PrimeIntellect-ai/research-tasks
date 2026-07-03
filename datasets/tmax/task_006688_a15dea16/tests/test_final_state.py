# test_final_state.py
import os
import subprocess
import time
import shutil

def test_prov_shim_binary_exists():
    binary_path = "/home/user/prov-shim/target/release/prov-shim"
    assert os.path.exists(binary_path), f"Rust binary not found at {binary_path}. Did you compile in release mode?"
    assert os.path.isfile(binary_path) and os.access(binary_path, os.X_OK), f"File at {binary_path} is not an executable."

def test_prov_shim_execution_and_artifacts():
    binary_path = "/home/user/prov-shim/target/release/prov-shim"
    workspace = "/home/user/eval_workspace"
    backup = "/home/user/eval_backup.tar.gz"
    port = "9988"
    extracted_dir = "/home/user/eval_extracted"

    # Clean up previous runs if any
    for path in [workspace, backup, extracted_dir]:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    start_time = time.time()
    try:
        proc = subprocess.run([binary_path, workspace, port, backup], capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        assert False, "The shim program timed out (ran for more than 15 seconds). It should run for exactly 5 seconds."
    elapsed = time.time() - start_time

    assert proc.returncode == 0, f"Shim executed with non-zero exit code. STDERR:\n{proc.stderr}"
    assert elapsed >= 5.0, f"Shim did not wait for the required 5 seconds. Elapsed time: {elapsed:.2f}s"

    assert os.path.exists(backup), f"Backup tarball not created at {backup}"

    os.makedirs(extracted_dir, exist_ok=True)
    extract_proc = subprocess.run(["tar", "-xzf", backup, "-C", extracted_dir], capture_output=True, text=True)
    assert extract_proc.returncode == 0, f"Failed to extract backup tarball. STDERR:\n{extract_proc.stderr}"

    status_file = os.path.join(extracted_dir, "status.txt")
    assert os.path.exists(status_file), "status.txt not found in the backup archive"
    with open(status_file, "r") as f:
        status_content = f.read().strip()
    assert status_content == "RUNNING", f"Expected status.txt to contain 'RUNNING', but got '{status_content}'"

    expected_gw = None
    with open("/proc/net/route", "r") as f:
        lines = f.readlines()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 3 and parts[1] == "00000000":
            expected_gw = parts[2]
            break

    assert expected_gw is not None, "Could not find default gateway (Destination 00000000) in /proc/net/route"

    gateway_file = os.path.join(extracted_dir, "gateway.info")
    assert os.path.exists(gateway_file), "gateway.info not found in the backup archive"
    with open(gateway_file, "r") as f:
        actual_gw = f.read().strip()

    assert actual_gw == expected_gw, f"Gateway mismatch in gateway.info: expected '{expected_gw}', got '{actual_gw}'"