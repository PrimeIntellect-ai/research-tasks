# test_final_state.py

import os
import time
import subprocess
import glob

def test_operator_execution_time_metric():
    """
    Runs the compiled Go operator and measures its execution time.
    Metric: Execution time (seconds)
    Threshold: <= 1.5 seconds
    """
    operator_path = '/home/user/operator'
    assert os.path.exists(operator_path), f"Compiled operator binary not found at {operator_path}"
    assert os.access(operator_path, os.X_OK), f"Operator binary at {operator_path} is not executable"

    env = os.environ.copy()
    env['TARGET_DIR'] = '/home/user/operator_data'
    env['BACKING_SIZE'] = '1024'

    # Clean up before run to ensure we measure actual creation time
    subprocess.run(['rm', '-rf', '/home/user/operator_data'], check=False)
    subprocess.run(['rm', '-f', '/home/user/fstab.mock'], check=False)
    subprocess.run(['rm', '-rf', '/home/user/active_mounts'], check=False)
    os.makedirs('/home/user/active_mounts', exist_ok=True)

    start = time.time()
    proc = subprocess.run([operator_path], env=env, capture_output=True, text=True)
    end = time.time()
    duration = end - start

    assert proc.returncode == 0, f"Operator execution failed with return code {proc.returncode}. Stderr: {proc.stderr}"

    assert duration <= 1.5, (
        f"Metric failed: runtime {duration:.2f}s > 1.5s threshold. "
        "Concurrency not properly implemented."
    )

def test_generated_files_and_size():
    """
    Verifies that the generated backing files exist in the correct directories
    and have the exact size specified by BACKING_SIZE.
    """
    target_dir = '/home/user/operator_data'
    assert os.path.isdir(target_dir), f"Target directory {target_dir} was not created."

    for i in range(1, 10001):
        ns = f"ns-{i % 20}"
        vol = f"vol-{i}"
        img_path = os.path.join(target_dir, ns, f"{vol}.img")

        assert os.path.exists(img_path), f"Backing file missing: {img_path}"

        size = os.path.getsize(img_path)
        assert size == 1024, f"File {img_path} size is {size}, expected exactly 1024 bytes."

def test_fstab_mock_contents():
    """
    Verifies that /home/user/fstab.mock contains the correct entries.
    """
    fstab_path = '/home/user/fstab.mock'
    assert os.path.exists(fstab_path), f"fstab.mock file not found at {fstab_path}"

    with open(fstab_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 10000, f"Expected 10000 lines in fstab.mock, found {len(lines)}"

    # Check a sample line
    sample_line = lines[0].strip()
    parts = sample_line.split()
    assert len(parts) == 6, f"Malformed fstab entry: {sample_line}"
    assert parts[0].startswith('/home/user/operator_data/'), f"Incorrect target dir in fstab: {parts[0]}"
    assert parts[2] == 'ext4', f"Incorrect filesystem type in fstab: {parts[2]}"
    assert parts[3] == 'loop,defaults', f"Incorrect mount options in fstab: {parts[3]}"

def test_active_mounts_symlinks():
    """
    Verifies that relative symlinks are created correctly in /home/user/active_mounts.
    """
    active_mounts_dir = '/home/user/active_mounts'
    assert os.path.isdir(active_mounts_dir), f"Directory {active_mounts_dir} not found"

    symlinks = glob.glob(os.path.join(active_mounts_dir, "vol-*"))
    assert len(symlinks) == 10000, f"Expected 10000 symlinks in {active_mounts_dir}, found {len(symlinks)}"

    # Check a sample symlink
    sample_symlink = os.path.join(active_mounts_dir, "vol-20")
    assert os.path.islink(sample_symlink), f"{sample_symlink} is not a symlink"

    target = os.readlink(sample_symlink)
    assert not os.path.isabs(target), f"Symlink target {target} is absolute, expected relative"

    # Resolve the symlink and check if it points to the correct file
    resolved_path = os.path.abspath(os.path.join(active_mounts_dir, target))
    expected_path = '/home/user/operator_data/ns-0/vol-20.img'
    assert resolved_path == expected_path, f"Symlink resolves to {resolved_path}, expected {expected_path}"

def test_run_operator_script_fixes():
    """
    Verifies that the bash script was updated to handle PATH, fail fast, and set env vars.
    """
    script_path = '/home/user/run_operator.sh'
    with open(script_path, 'r') as f:
        content = f.read()

    assert 'set -e' in content or 'set -Eeuo pipefail' in content, "Script does not contain fail-fast error handling (e.g., set -e)"
    assert 'PATH=' in content, "Script does not explicitly set or export PATH"
    assert 'TARGET_DIR=' in content, "Script does not set TARGET_DIR"
    assert 'BACKING_SIZE=' in content, "Script does not set BACKING_SIZE"