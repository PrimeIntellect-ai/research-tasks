# test_final_state.py

import os
import re
import subprocess
import tarfile
import pytest

def test_scripts_are_executable():
    """Check that all required scripts are executable."""
    scripts = [
        "/home/user/diagnose.py",
        "/home/user/backup.sh",
        "/home/user/provision_disk.sh",
        "/home/user/launch_qemu.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_diagnose_py_output():
    """Test that diagnose.py correctly identifies the IP address."""
    script_path = "/home/user/diagnose.py"
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed to execute."

    output = result.stdout.strip()
    assert output == "10.0.0.5", f"Expected output '10.0.0.5', got '{output}'"

def test_backup_sh_creates_tarball():
    """Test that backup.sh creates the correct tarball."""
    script_path = "/home/user/backup.sh"
    tarball_path = "/home/user/manifests_backup.tar.gz"

    # Remove if exists to ensure the script creates it
    if os.path.exists(tarball_path):
        os.remove(tarball_path)

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed to execute."
    assert os.path.isfile(tarball_path), f"Tarball {tarball_path} was not created."

    # Check tarball contents
    with tarfile.open(tarball_path, "r:gz") as tar:
        names = tar.getnames()
        # Should contain manifests directory or its contents
        assert any("manifests" in name for name in names), "Tarball does not contain 'manifests'."

def test_new_fstab_content():
    """Test that new_fstab contains the correct entry."""
    fstab_path = "/home/user/new_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    # Normalize whitespace for comparison
    normalized_content = re.sub(r'\s+', ' ', content)
    expected = "LABEL=vmdatalocal /var/lib/vmdata ext4 rw,noatime 0 2"
    assert normalized_content == expected, f"Expected fstab entry '{expected}', got '{normalized_content}'"

def test_provision_disk_sh():
    """Test that provision_disk.sh creates an ext4 formatted disk image."""
    script_path = "/home/user/provision_disk.sh"
    disk_path = "/home/user/vm_disk.img"

    if os.path.exists(disk_path):
        os.remove(disk_path)

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed to execute."
    assert os.path.isfile(disk_path), f"Disk image {disk_path} was not created."

    # Check size (approx 50MB)
    size = os.path.getsize(disk_path)
    assert size >= 45 * 1024 * 1024, f"Disk image size {size} is less than expected ~50MB."

    # Check filesystem type using `file`
    file_cmd = subprocess.run(["file", disk_path], capture_output=True, text=True)
    assert "ext4 filesystem" in file_cmd.stdout.lower(), f"Disk image is not formatted as ext4. Output: {file_cmd.stdout}"

def test_launch_qemu_sh_content():
    """Test that launch_qemu.sh contains the correct QEMU arguments."""
    script_path = "/home/user/launch_qemu.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "qemu-system-x86_64" in content, "Missing 'qemu-system-x86_64' command."
    assert "-vnc" in content and ":2" in content, "Missing VNC configuration for display :2."
    assert "vm_disk.img" in content, "Missing disk image attachment."
    assert "virtio" in content, "Missing 'virtio' block device configuration."
    assert "qemu.pid" in content, "Missing PID file configuration."
    assert "-nographic" in content or "-display none" in content, "Missing flag to disable default graphical UI."