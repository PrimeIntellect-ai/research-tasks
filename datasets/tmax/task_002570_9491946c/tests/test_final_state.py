# test_final_state.py

import os
import subprocess
import pytest

def test_post_receive_exists_and_executable():
    hook_path = "/home/user/uptime.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"The git hook binary {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"The git hook binary {hook_path} is not executable."

def test_post_receive_logic():
    hook_path = "/home/user/uptime.git/hooks/post-receive"
    output_path = "/home/user/reports_dir/latest.txt"

    # Remove the output file if it exists to ensure the hook actually creates/writes it
    if os.path.exists(output_path):
        os.remove(output_path)

    # Execute the hook
    try:
        subprocess.run([hook_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executing the hook failed with exit code {e.returncode}. Stderr: {e.stderr}")

    assert os.path.isfile(output_path), f"The hook did not create the expected output file at {output_path}."

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "Uptime: 80%", f"Expected 'Uptime: 80%', but found '{content}' in {output_path}."

def test_setup_tunnel_script():
    script_path = "/home/user/setup_tunnel.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    expected_command = "ssh -N -f -L 9999:localhost:8000 user@localhost"
    assert expected_command in content, f"The script {script_path} does not contain the correct SSH port forwarding command."