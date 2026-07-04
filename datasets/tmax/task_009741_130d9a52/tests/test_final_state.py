# test_final_state.py

import os
import pytest

def test_firewall_rules_updated():
    rules_path = '/home/user/active_firewall.rules'
    assert os.path.isfile(rules_path), f"File {rules_path} does not exist. The exploit may not have triggered the server's success condition."

    with open(rules_path, 'r') as f:
        content = f.read()

    assert "ALLOW 10.9.8.7" in content, f"File {rules_path} does not contain the expected 'ALLOW 10.9.8.7' rule."

def test_flag_file_created_and_correct():
    flag_path = '/home/user/flag.txt'
    assert os.path.isfile(flag_path), f"File {flag_path} does not exist. Ensure your exploit saves the server's response."

    with open(flag_path, 'r') as f:
        content = f.read()

    assert "FLAG{cxx_n0n3_alg_byt3s}" in content, f"File {flag_path} does not contain the correct flag. The exploit might have failed or the response was not saved correctly."

def test_exploit_cpp_exists_and_valid():
    exploit_path = '/home/user/exploit.cpp'
    assert os.path.isfile(exploit_path), f"File {exploit_path} does not exist. You must write your exploit script at this exact path."

    with open(exploit_path, 'r') as f:
        content = f.read()

    assert "#include" in content, f"File {exploit_path} does not appear to be a valid C++ source file (missing '#include')."