# test_final_state.py

import os
import subprocess
import pytest

DEPLOY_SCRIPT = "/home/user/deploy_update.py"
RUN_SCRIPT = "/home/user/run_deployment.sh"
ROUTE_CONFIG = "/home/user/route_config.cmds"

def test_scripts_exist_and_executable():
    """Verify that both scripts exist and the bash wrapper is executable."""
    assert os.path.isfile(DEPLOY_SCRIPT), f"{DEPLOY_SCRIPT} does not exist."
    assert os.path.isfile(RUN_SCRIPT), f"{RUN_SCRIPT} does not exist."
    assert os.access(RUN_SCRIPT, os.X_OK), f"{RUN_SCRIPT} is not executable."

def test_run_deployment_creates_config():
    """Verify that running the bash wrapper creates the expected route config file."""
    # Ensure the config file doesn't exist before running, or remove it to test fresh creation
    if os.path.exists(ROUTE_CONFIG):
        os.remove(ROUTE_CONFIG)

    result = subprocess.run([RUN_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"{RUN_SCRIPT} failed with exit code {result.returncode}. stderr: {result.stderr}"

    assert os.path.isfile(ROUTE_CONFIG), f"{ROUTE_CONFIG} was not created by {RUN_SCRIPT}."

    expected_content = (
        "ip link add name deploy0 type dummy\n"
        "ip link set deploy0 up\n"
        "ip route add 10.150.0.0/16 dev deploy0\n"
    )

    with open(ROUTE_CONFIG, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), (
        f"Contents of {ROUTE_CONFIG} do not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )

def test_deploy_update_wrong_env():
    """Verify that deploy_update.py exits with 1 when environment variables do not match."""
    env = os.environ.copy()
    env["TZ"] = "UTC"
    env["LC_ALL"] = "en_US.UTF-8"

    result = subprocess.run(["python3", DEPLOY_SCRIPT], env=env, capture_output=True, text=True)
    assert result.returncode == 1, (
        f"{DEPLOY_SCRIPT} should exit with code 1 when TZ and LC_ALL do not match, "
        f"but exited with {result.returncode}."
    )

def test_deploy_update_wrong_input():
    """Verify that deploy_update.py exits with 1 when user inputs something other than 'Y'."""
    env = os.environ.copy()
    env["TZ"] = "America/New_York"
    env["LC_ALL"] = "fr_CA.UTF-8"

    result = subprocess.run(
        ["python3", DEPLOY_SCRIPT], 
        env=env, 
        input="n\n", 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 1, (
        f"{DEPLOY_SCRIPT} should exit with code 1 when input is not 'Y', "
        f"but exited with {result.returncode}."
    )
    assert "Region detected. Confirm deployment? [Y/n]:" in result.stdout or "Region detected. Confirm deployment? [Y/n]:" in result.stderr, \
        "The script did not prompt with the exact required string."