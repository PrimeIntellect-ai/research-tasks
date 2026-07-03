# test_final_state.py
import os
import pytest

def test_port_txt():
    port_file = "/home/user/port.txt"
    assert os.path.isfile(port_file), f"{port_file} does not exist."

    with open(port_file, "r") as f:
        content = f.read().strip()

    assert content == "8432", f"Expected port 8432 in {port_file}, but found '{content}'."

def test_attacker_ips():
    ips_file = "/home/user/attacker_ips.txt"
    assert os.path.isfile(ips_file), f"{ips_file} does not exist."

    with open(ips_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_ips = [
        "10.0.0.99",
        "172.16.0.42",
        "203.0.113.8"
    ]

    assert lines == expected_ips, f"Expected {expected_ips} in {ips_file}, but found {lines}."

def test_process_logs_go_exists():
    go_file = "/home/user/process_logs.go"
    assert os.path.isfile(go_file), f"The Go program {go_file} does not exist."