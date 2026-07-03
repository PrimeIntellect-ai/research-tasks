# test_final_state.py

import os
import struct
import pytest

def test_payload_bin_content():
    payload_bin_path = "/home/user/payload.bin"
    assert os.path.isfile(payload_bin_path), f"File {payload_bin_path} is missing. The payload was not decrypted."

    # Recreate the expected plain bytes
    c2_ip = bytes([192, 168, 137, 42])
    c2_port = struct.pack('!H', 4444)
    expected_plain = (
        b'\x7FELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00' + 
        b'A' * 50 + 
        b'C2_START' + 
        c2_ip + 
        c2_port + 
        b'B' * 20
    )

    with open(payload_bin_path, 'rb') as f:
        actual_plain = f.read()

    assert actual_plain == expected_plain, "The decrypted payload in /home/user/payload.bin does not match the expected plaintext."

def test_firewall_rule_content():
    firewall_rule_path = "/home/user/firewall_rule.txt"
    assert os.path.isfile(firewall_rule_path), f"File {firewall_rule_path} is missing. The firewall rule was not saved."

    expected_rule = "iptables -A OUTPUT -d 192.168.137.42 -p tcp --dport 4444 -j DROP"

    with open(firewall_rule_path, 'r') as f:
        actual_rule = f.read().strip()

    assert actual_rule == expected_rule, f"The firewall rule in {firewall_rule_path} is incorrect. Expected: '{expected_rule}', but got: '{actual_rule}'"