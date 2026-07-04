# test_final_state.py
import os
import json
import subprocess

def test_script_exists():
    assert os.path.isfile('/home/user/run_mtu_check.py'), "The script /home/user/run_mtu_check.py does not exist."

def test_script_execution_and_idempotency():
    # Run the script from /tmp to test path independence
    try:
        subprocess.run(
            ['python3', '/home/user/run_mtu_check.py'],
            cwd='/tmp',
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        assert False, f"Script execution failed with error: {e.stderr}"

def test_directory_structure():
    target_dir = '/home/user/app_data/network_logs'
    assert os.path.isdir(target_dir), f"Directory {target_dir} does not exist."

def test_symlink_state():
    symlink_path = '/home/user/current_logs'
    target_dir = '/home/user/app_data/network_logs'

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    assert os.readlink(symlink_path) == target_dir, f"Symlink {symlink_path} does not point to {target_dir}."

def test_mtu_json_content():
    json_path = '/home/user/current_logs/mtu.json'
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            agent_mtu = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} does not contain valid JSON."

    # Get ground truth
    try:
        output = subprocess.check_output(['ip', '-j', 'link', 'show']).decode('utf-8')
        data = json.loads(output)
        expected_mtu = {iface['ifname']: iface['mtu'] for iface in data}
    except Exception as e:
        assert False, f"Failed to retrieve ground truth MTU data: {e}"

    assert agent_mtu == expected_mtu, f"MTU data mismatch. Expected {expected_mtu}, but got {agent_mtu}."