# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_ssh_key_permissions_fixed():
    private_key = "/home/user/.ssh/id_rsa"
    assert os.path.exists(private_key), f"Private key {private_key} is missing."

    st = os.stat(private_key)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Permissions for {private_key} are not 600. Current permissions: {oct(perms)}. SSH will reject an open private key."

def test_mount_directory_created():
    fstab_file = "/home/user/network_fstab"
    assert os.path.exists(fstab_file), f"{fstab_file} is missing."

    # Parse the fstab file to find the expected mount point dynamically
    expected_mount = None
    with open(fstab_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 2 and parts[0] == "//storage-node/router-backups":
                    expected_mount = parts[1]
                    break

    assert expected_mount is not None, "Could not find //storage-node/router-backups in fstab."
    assert os.path.isdir(expected_mount), f"The mount directory {expected_mount} does not exist or is not a directory."

def test_python_script_behavior():
    script_path = "/home/user/net_manager.py"
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

    # Remove the backup file if it exists from previous manual runs
    fstab_file = "/home/user/network_fstab"
    expected_mount = None
    with open(fstab_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 2 and parts[0] == "//storage-node/router-backups":
                    expected_mount = parts[1]
                    break

    backup_file = os.path.join(expected_mount, "router-01-latest.bak")
    if os.path.exists(backup_file):
        os.remove(backup_file)

    # Run the script with simulated stdin
    input_data = "UNKNOWN\nBACKUP\nEXIT\n"

    try:
        result = subprocess.run(
            ["python3", script_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=10,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script exited with non-zero return code {e.returncode}. Stderr: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Script timed out. Ensure it exits when receiving 'EXIT'.")

    stdout = result.stdout.strip().split('\n')
    stdout = [line.strip() for line in stdout if line.strip()]

    assert len(stdout) >= 2, f"Expected at least two lines of output, got: {stdout}"
    assert "UNKNOWN_COMMAND" in stdout[0], f"Expected UNKNOWN_COMMAND for unknown input, got: {stdout[0]}"
    assert "BACKUP_SUCCESS" in stdout[1], f"Expected BACKUP_SUCCESS after backup command, got: {stdout[1]}"

    # Verify the backup file was created and matches the source
    assert os.path.isfile(backup_file), f"Backup file {backup_file} was not created."

    source_file = "/home/user/router_config.txt"
    with open(source_file, 'r') as f:
        expected_content = f.read()

    with open(backup_file, 'r') as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"Content of {backup_file} does not match {source_file}."