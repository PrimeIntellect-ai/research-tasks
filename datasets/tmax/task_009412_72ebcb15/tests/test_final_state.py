# test_final_state.py

import os
import pytest

def test_attacker_ip_file():
    target_file = '/home/user/attacker_ip.txt'
    assert os.path.isfile(target_file), f"The file {target_file} does not exist."

    with open(target_file, 'r') as f:
        content = f.read().strip()

    expected_ip = "172.16.45.99"
    assert content == expected_ip, f"Expected attacker IP '{expected_ip}', but found '{content}' in {target_file}."

def test_flag_file():
    target_file = '/home/user/flag.txt'
    assert os.path.isfile(target_file), f"The file {target_file} does not exist."

    with open(target_file, 'r') as f:
        content = f.read().strip()

    expected_flag = "FLAG{b4sh_l0g_f0r3ns1cs}"
    assert content == expected_flag, f"Expected flag '{expected_flag}', but found '{content}' in {target_file}."