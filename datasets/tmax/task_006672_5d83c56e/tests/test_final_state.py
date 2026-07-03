# test_final_state.py

import os
import re
import subprocess
import pytest

BASH_PROFILE = "/home/user/.bash_profile"
DEPLOY_SCRIPT = "/home/user/deploy_microservice.py"
QEMU_LOG = "/home/user/qemu_cmd.log"

def test_bash_profile_exports():
    """Verify that .bash_profile exports the correct environment variables."""
    assert os.path.exists(BASH_PROFILE), f"{BASH_PROFILE} does not exist."

    with open(BASH_PROFILE, "r") as f:
        content = f.read()

    mem_match = re.search(r'export\s+MICRO_MEM=[\'"]?512M[\'"]?', content)
    port_match = re.search(r'export\s+MICRO_VNC_PORT=[\'"]?5[\'"]?', content)

    assert mem_match is not None, f"MICRO_MEM not correctly exported in {BASH_PROFILE}."
    assert port_match is not None, f"MICRO_VNC_PORT not correctly exported in {BASH_PROFILE}."

def test_deploy_script_exists():
    """Verify that the deploy_microservice.py script exists."""
    assert os.path.exists(DEPLOY_SCRIPT), f"{DEPLOY_SCRIPT} does not exist."
    assert os.path.isfile(DEPLOY_SCRIPT), f"{DEPLOY_SCRIPT} is not a file."

def test_qemu_log_content():
    """Verify that qemu_cmd.log contains the correct command string from the initial run."""
    assert os.path.exists(QEMU_LOG), f"{QEMU_LOG} does not exist."

    with open(QEMU_LOG, "r") as f:
        content = f.read().strip()

    expected_cmd = "qemu-system-x86_64 -m 512M -vnc 127.0.0.1:5 -daemonize -display none"
    assert content == expected_cmd, f"Expected '{expected_cmd}', but found '{content}' in {QEMU_LOG}."

def test_python_script_fallback_behavior():
    """Verify that the deploy script uses correct default values when env vars are unset."""
    # Ensure the script is executable or we run it with python3
    env = os.environ.copy()
    env.pop("MICRO_MEM", None)
    env.pop("MICRO_VNC_PORT", None)

    result = subprocess.run(["python3", DEPLOY_SCRIPT], env=env, capture_output=True, text=True)
    assert result.returncode == 0, f"Running {DEPLOY_SCRIPT} failed with error: {result.stderr}"

    assert os.path.exists(QEMU_LOG), f"{QEMU_LOG} does not exist after running script."

    with open(QEMU_LOG, "r") as f:
        content = f.read().strip()

    expected_fallback_cmd = "qemu-system-x86_64 -m 256M -vnc 127.0.0.1:1 -daemonize -display none"
    assert content == expected_fallback_cmd, (
        f"Fallback behavior failed. Expected '{expected_fallback_cmd}', "
        f"but found '{content}' in {QEMU_LOG}."
    )