# test_final_state.py
import os
import tarfile
import pytest

REDACTED_LOG = "/home/user/redacted.log"
SUCCESS_IDS = "/home/user/successful_job_ids.txt"
TARBALL = "/home/user/backup_report.tar.gz"

def test_redacted_log():
    assert os.path.exists(REDACTED_LOG), f"{REDACTED_LOG} does not exist."
    assert os.path.isfile(REDACTED_LOG), f"{REDACTED_LOG} is not a file."

    with open(REDACTED_LOG, 'r') as f:
        content = f.read()

    assert "192.168.1.10" not in content, "Real IP 192.168.1.10 was not redacted."
    assert "10.0.0.55" not in content, "Real IP 10.0.0.55 was not redacted."
    assert "172.16.254.1" not in content, "Real IP 172.16.254.1 was not redacted."

    lines = content.strip().split('\n')
    server_ip_lines = [line for line in lines if line.startswith("ServerIP:")]
    assert len(server_ip_lines) == 4, "Expected 4 ServerIP lines in the redacted log."
    for line in server_ip_lines:
        assert line == "ServerIP: XXX.XXX.XXX.XXX", f"Invalid redaction format: {line}"

def test_successful_job_ids():
    assert os.path.exists(SUCCESS_IDS), f"{SUCCESS_IDS} does not exist."
    assert os.path.isfile(SUCCESS_IDS), f"{SUCCESS_IDS} is not a file."

    with open(SUCCESS_IDS, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ids = ["1041", "1045", "1048"]
    assert lines == expected_ids, f"Expected successful job IDs {expected_ids}, got {lines}"

def test_tarball_archive():
    assert os.path.exists(TARBALL), f"{TARBALL} does not exist."
    assert os.path.isfile(TARBALL), f"{TARBALL} is not a file."
    assert tarfile.is_tarfile(TARBALL), f"{TARBALL} is not a valid tar archive."

    with tarfile.open(TARBALL, "r:gz") as tar:
        members = tar.getmembers()
        assert len(members) == 1, f"Expected exactly 1 file in tarball, found {len(members)}."

        member = members[0]
        assert member.name == "successful_job_ids.txt", f"Expected file named 'successful_job_ids.txt' at root of tarball, got '{member.name}'."

        f = tar.extractfile(member)
        assert f is not None, "Could not extract file from tarball."
        content = f.read().decode('utf-8')

        lines = [line.strip() for line in content.split('\n') if line.strip()]
        expected_ids = ["1041", "1045", "1048"]
        assert lines == expected_ids, f"Tarball content mismatch. Expected {expected_ids}, got {lines}"