# test_final_state.py
import os
import stat
import subprocess

def test_01_setup_script():
    setup_script = "/home/user/setup.sh"
    assert os.path.isfile(setup_script), f"{setup_script} does not exist"
    assert os.access(setup_script, os.X_OK), f"{setup_script} is not executable"

    # Run setup script
    result = subprocess.run([setup_script], capture_output=True, text=True)
    assert result.returncode == 0, f"{setup_script} failed with exit code {result.returncode}"

    state_file = "/home/user/service_data/state.dat"
    assert os.path.isfile(state_file), f"{state_file} was not created"

    with open(state_file, "r") as f:
        content = f.read().strip()
    assert content == "READY", f"Expected state.dat to contain 'READY', but got '{content}'"

    # Run again to check idempotency
    result2 = subprocess.run([setup_script], capture_output=True, text=True)
    assert result2.returncode == 0, "Setup script is not idempotent (failed on second run)"

def test_02_monitor():
    monitor_bin = "/home/user/monitor"
    assert os.path.isfile(monitor_bin), f"{monitor_bin} does not exist"
    assert os.access(monitor_bin, os.X_OK), f"{monitor_bin} is not executable"

    # state.dat should currently be READY from test_01
    result = subprocess.run([monitor_bin], capture_output=True, text=True)
    assert result.returncode == 0, f"Monitor exited with {result.returncode}, expected 0"
    assert "HEALTHY" in result.stdout, f"Expected output 'HEALTHY', got '{result.stdout}'"

def test_03_backup_script():
    backup_script = "/home/user/backup.sh"
    assert os.path.isfile(backup_script), f"{backup_script} does not exist"
    assert os.access(backup_script, os.X_OK), f"{backup_script} is not executable"

    # Run backup script
    result = subprocess.run([backup_script], capture_output=True, text=True)
    assert result.returncode == 0, f"{backup_script} failed with exit code {result.returncode}"

    backup_archive = "/home/user/backup.tar.gz"
    assert os.path.isfile(backup_archive), f"{backup_archive} was not created"

def test_04_restore_script():
    restore_script = "/home/user/restore.exp"
    state_file = "/home/user/service_data/state.dat"
    monitor_bin = "/home/user/monitor"

    assert os.path.isfile(restore_script), f"{restore_script} does not exist"
    assert os.access(restore_script, os.X_OK), f"{restore_script} is not executable"

    # Break the state
    with open(state_file, "w") as f:
        f.write("BROKEN\n")

    # Verify monitor catches it
    result_broken = subprocess.run([monitor_bin], capture_output=True, text=True)
    assert result_broken.returncode == 1, "Monitor did not exit with 1 when state was broken"
    assert "CORRUPT" in result_broken.stdout, "Monitor did not output 'CORRUPT' when state was broken"

    # Run restore script
    result_restore = subprocess.run([restore_script], capture_output=True, text=True)
    assert result_restore.returncode == 0, f"{restore_script} failed with exit code {result_restore.returncode}"

    # Verify state is restored
    with open(state_file, "r") as f:
        content = f.read().strip()
    assert content == "READY", f"State was not restored properly, got '{content}'"

    # Verify monitor is happy again
    result_fixed = subprocess.run([monitor_bin], capture_output=True, text=True)
    assert result_fixed.returncode == 0, "Monitor did not exit with 0 after restore"
    assert "HEALTHY" in result_fixed.stdout, "Monitor did not output 'HEALTHY' after restore"