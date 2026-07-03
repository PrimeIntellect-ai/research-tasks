# test_final_state.py

import os
import stat
import re
import pytest

def test_decoder_cpp_exists():
    assert os.path.isfile("/home/user/decoder.cpp"), "The C++ program /home/user/decoder.cpp is missing."

def test_recovered_txt():
    recovered_path = "/home/user/recovered.txt"
    assert os.path.isfile(recovered_path), f"The file {recovered_path} is missing."
    with open(recovered_path, "r") as f:
        content = f.read().strip()
    assert content == "root_db_pass:Sup3rS3cr3t!99", "The decrypted content in recovered.txt is incorrect."

def test_block_ip_script():
    script_path = "/home/user/block_ip.sh"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."
    with open(script_path, "r") as f:
        content = f.read()

    # Check for iptables command
    match = re.search(r'iptables\s+-A\s+OUTPUT\s+-d\s+198\.51\.100\.77\s+-j\s+DROP', content)
    assert match is not None, "The block_ip.sh script does not contain the correct iptables command to drop traffic to 198.51.100.77."

def test_authorized_keys_content():
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys_path), f"The file {auth_keys_path} is missing."
    with open(auth_keys_path, "r") as f:
        content = f.read()

    assert "attacker@exfil-server" not in content, "The attacker's SSH key was not removed from authorized_keys."
    assert "user@legitimate-machine" in content, "A legitimate SSH key (user@legitimate-machine) was incorrectly removed."
    assert "admin@jumpbox" in content, "A legitimate SSH key (admin@jumpbox) was incorrectly removed."

def test_authorized_keys_permissions():
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys_path), f"The file {auth_keys_path} is missing."

    st = os.stat(auth_keys_path)
    permissions = stat.S_IMODE(st.st_mode)

    assert permissions == 0o600, f"The permissions of {auth_keys_path} are incorrect. Expected 600, got {oct(permissions)}."