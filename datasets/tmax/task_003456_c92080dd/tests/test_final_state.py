# test_final_state.py
import os
import json
import pytest

def test_symlink_points_to_v2():
    symlink_path = '/home/user/deployments/active'
    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symbolic link."

    target = os.readlink(symlink_path)
    # The target could be absolute or relative, but the instructions imply updating it to point to v2.conf.
    # We will check if the resolved path points to the correct absolute path.
    resolved_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
    expected_target = '/home/user/deployments/v2.conf'

    assert resolved_target == expected_target, (
        f"Symlink {symlink_path} points to {resolved_target}, expected {expected_target}."
    )

def test_router_state_json_matches_v2_conf():
    state_file = '/home/user/router_state.json'
    v2_conf_file = '/home/user/deployments/v2.conf'

    assert os.path.isfile(state_file), f"Expected router state file {state_file} does not exist. Did the commit succeed?"
    assert os.path.isfile(v2_conf_file), f"Expected configuration file {v2_conf_file} is missing."

    with open(v2_conf_file, 'r') as f:
        expected_lines = [line.strip() for line in f if line.strip()]

    with open(state_file, 'r') as f:
        try:
            state_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {state_file} is not valid JSON.")

    assert "active_config" in state_data, f"'active_config' key missing from {state_file}."

    actual_config = state_data["active_config"]
    assert actual_config == expected_lines, (
        f"The committed configuration in {state_file} does not match the contents of {v2_conf_file}.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_config}"
    )