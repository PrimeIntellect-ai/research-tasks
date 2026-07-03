# test_final_state.py
import os
import pytest

def test_net_users_conf_updated():
    conf_path = "/home/user/net_users.conf"
    assert os.path.exists(conf_path), f"File {conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read().strip()

    expected_content = """alice:admin,users
bob:users
charlie:dev,users,netadmin
diana:netadmin,users"""

    assert content == expected_content, f"Content of {conf_path} does not match expected output."

def test_failed_ips_created():
    failed_ips_path = "/home/user/failed_ips.txt"
    assert os.path.exists(failed_ips_path), f"File {failed_ips_path} is missing."

    with open(failed_ips_path, "r") as f:
        content = f.read().strip()

    expected_content = """10.0.0.5\n10.10.10.10\n172.16.0.2"""
    assert content == expected_content, f"Content of {failed_ips_path} does not match expected extracted IPs."

def test_probe_log_archive_created():
    archive_path = "/home/user/probe.log.archive"
    assert os.path.exists(archive_path), f"File {archive_path} is missing."

    with open(archive_path, "r") as f:
        content = f.read().strip()

    expected_content = """2023-10-01T10:00:00 192.168.1.10 OK
2023-10-01T10:01:00 10.0.0.5 TIMEOUT
2023-10-01T10:02:00 172.16.0.2 DROP
2023-10-01T10:03:00 10.0.0.5 TIMEOUT
2023-10-01T10:04:00 192.168.1.20 OK
2023-10-01T10:05:00 10.10.10.10 DROP
2023-10-01T10:06:00 192.168.1.10 OK"""

    assert content == expected_content, f"Content of {archive_path} does not match the original log."

def test_probe_log_cleared():
    probe_log_path = "/home/user/probe.log"
    assert os.path.exists(probe_log_path), f"File {probe_log_path} is missing."
    assert os.path.getsize(probe_log_path) == 0, f"File {probe_log_path} is not empty."