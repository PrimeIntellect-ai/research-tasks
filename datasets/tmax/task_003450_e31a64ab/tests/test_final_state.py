# test_final_state.py
import os
import subprocess
import re
import shutil

def test_expect_script():
    expect_script = "/home/user/check_vm.exp"
    assert os.path.exists(expect_script), f"{expect_script} does not exist."

    # Run expect script
    result = subprocess.run(["expect", expect_script], capture_output=True, text=True)
    assert "BOOT SUCCESS" in result.stdout, "Expect script failed to boot the VM successfully. Output:\n" + result.stdout

def test_rust_binary_exists():
    binary_path = "/home/user/vm_monitor/target/debug/vm_monitor"
    assert os.path.exists(binary_path), f"Rust binary not found at {binary_path}."
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable."

def test_rust_binary_logic():
    binary_path = "/home/user/vm_monitor/target/debug/vm_monitor"
    log_path = "/home/user/alerts.log"
    mock_qemu_path = "/home/user/bin/mock_qemu"
    backup_path = "/home/user/bin/mock_qemu.bak"

    # Ensure log is clean before test
    if os.path.exists(log_path):
        os.remove(log_path)

    # Run success case (mock_qemu should succeed via expect script)
    subprocess.run([binary_path], capture_output=True)
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            content = f.read()
            assert "ALERT: VM boot failed" not in content, "Alert logged when boot should have succeeded."

    # Backup original mock_qemu
    shutil.copy(mock_qemu_path, backup_path)

    try:
        # Create failing mock_qemu to simulate failure
        with open(mock_qemu_path, 'w') as f:
            f.write("#!/bin/bash\necho 'KERNEL PANIC - not syncing'\nexit 1\n")

        # Run failure case
        subprocess.run([binary_path], capture_output=True)

        assert os.path.exists(log_path), "Alert log not created on failure."
        with open(log_path, 'r') as f:
            content = f.read()
            assert "ALERT: VM boot failed" in content, "Alert log does not contain the correct message on failure."

    finally:
        # Restore original mock_qemu
        shutil.move(backup_path, mock_qemu_path)

def test_cron_schedule():
    cron_file = "/home/user/monitor_cron"
    assert os.path.exists(cron_file), f"{cron_file} not found."

    with open(cron_file, 'r') as f:
        content = f.read()

    # Look for every 5 minutes syntax
    pattern = r"^\s*\*/5\s+\*\s+\*\s+\*\s+\*\s+/home/user/vm_monitor/target/debug/vm_monitor\s*$"
    match = re.search(pattern, content, re.MULTILINE)
    assert match is not None, "Cron schedule is incorrect or missing in /home/user/monitor_cron."