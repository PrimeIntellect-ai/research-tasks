# test_final_state.py

import os
import pytest

def test_run_sim_script_exists():
    assert os.path.isfile("/home/user/run_sim.py"), "The script /home/user/run_sim.py does not exist."

def test_js_distance_output():
    user_file = "/home/user/js_distance.txt"
    expected_file = "/tmp/js_distance_expected.txt"

    assert os.path.isfile(user_file), f"The output file {user_file} does not exist."
    assert os.path.isfile(expected_file), f"The expected file {expected_file} is missing from the environment."

    with open(user_file, 'r') as f:
        user_val = f.read().strip()

    with open(expected_file, 'r') as f:
        expected_val = f.read().strip()

    assert user_val == expected_val, f"Expected JS distance {expected_val}, but got {user_val}."

def test_node0_c_output():
    user_file = "/home/user/node0_c.txt"
    expected_file = "/tmp/node0_c_expected.txt"

    assert os.path.isfile(user_file), f"The output file {user_file} does not exist."
    assert os.path.isfile(expected_file), f"The expected file {expected_file} is missing from the environment."

    with open(user_file, 'r') as f:
        user_val = f.read().strip()

    with open(expected_file, 'r') as f:
        expected_val = f.read().strip()

    assert user_val == expected_val, f"Expected node 0 concentration {expected_val}, but got {user_val}."