# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/generate_vm_configs.py"
CONFIGS_DIR = "/home/user/configs"

def test_script_exists():
    """Ensure the Python script exists at the correct path."""
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

def test_script_execution_and_output():
    """Test executing the script and verifying its outputs."""
    vm_name = "pytest_vm"
    timezone = "Asia/Tokyo"
    admin_email = "test@example.com"

    # Execute the script
    result = subprocess.run(
        ["python3", SCRIPT_PATH, vm_name, timezone, admin_email],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    # Check directory
    assert os.path.exists(CONFIGS_DIR), f"Directory {CONFIGS_DIR} was not created."
    assert os.path.isdir(CONFIGS_DIR), f"{CONFIGS_DIR} is not a directory."

    # Check fstab
    fstab_path = os.path.join(CONFIGS_DIR, f"{vm_name}_fstab")
    assert os.path.exists(fstab_path), f"fstab file {fstab_path} was not created."
    with open(fstab_path, "r") as f:
        fstab_content = f.read().strip()
    expected_fstab = f"/var/lib/qemu/images/{vm_name}.img /mnt/{vm_name} ext4 loop,noexec,nosuid,nodev 0 0"
    assert fstab_content == expected_fstab, f"fstab content mismatch. Expected: '{expected_fstab}', Got: '{fstab_content}'"

    # Check aliases
    aliases_path = os.path.join(CONFIGS_DIR, f"{vm_name}_aliases")
    assert os.path.exists(aliases_path), f"aliases file {aliases_path} was not created."
    with open(aliases_path, "r") as f:
        aliases_content = f.read().strip()
    expected_aliases = f"vm-{vm_name}-alerts: {admin_email}"
    assert aliases_content == expected_aliases, f"aliases content mismatch. Expected: '{expected_aliases}', Got: '{aliases_content}'"

    # Check apply.sh
    apply_sh_path = os.path.join(CONFIGS_DIR, f"{vm_name}_apply.sh")
    assert os.path.exists(apply_sh_path), f"apply.sh file {apply_sh_path} was not created."

    # Check permissions
    st = os.stat(apply_sh_path)
    file_permissions = oct(st.st_mode)[-3:]
    assert file_permissions == "755", f"apply.sh permissions are not 0755. Got: {file_permissions}"

    with open(apply_sh_path, "r") as f:
        apply_sh_content = f.read()

    assert apply_sh_content.startswith("#!/bin/bash"), "apply.sh does not start with #!/bin/bash"
    assert f'TZ="{timezone}"' in apply_sh_content or f"TZ={timezone}" in apply_sh_content, "Missing or incorrect TZ assignment in apply.sh"
    assert "export TZ" in apply_sh_content, "TZ is not exported in apply.sh"
    assert f'read -p "Proceed with hardening {vm_name}? (y/n): " confirm' in apply_sh_content, "Missing correct read prompt in apply.sh"
    assert f'echo "Hardening applied for {vm_name}"' in apply_sh_content or f"echo 'Hardening applied for {vm_name}'" in apply_sh_content, "Missing correct echo statement in apply.sh"