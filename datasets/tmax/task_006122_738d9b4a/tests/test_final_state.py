# test_final_state.py

import os

def test_flag_file_exists():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"The flag file {flag_path} does not exist. Ensure your PoC saves the retrieved flag to this location."

def test_flag_content():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), "Cannot check content because flag.txt is missing."

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{inc1d3nt_r3sp0ns3_ch41n_m4st3r}"
    assert expected_flag in content, f"The flag file does not contain the correct flag. Found: {content}"

def test_poc_script_exists():
    poc_path = "/home/user/poc.py"
    assert os.path.isfile(poc_path), f"The PoC script {poc_path} does not exist. Ensure you wrote the exploit script as requested."