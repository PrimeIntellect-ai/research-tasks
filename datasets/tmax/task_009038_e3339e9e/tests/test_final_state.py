# test_final_state.py

import os
import re
import tarfile
import pytest

def test_archive_manifest_content():
    manifest_path = "/home/user/archive_manifest.txt"
    data_dir = "/home/user/recovery/data"

    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    expected_lines = []
    if os.path.isdir(data_dir):
        for filename in os.listdir(data_dir):
            if filename.endswith(".dat"):
                filepath = os.path.join(data_dir, filename)
                if os.path.isfile(filepath) and os.path.getsize(filepath) > 10240:
                    with open(filepath, "rb") as f:
                        header = f.read(4).hex().lower()
                    expected_lines.append(f"{filename}: {header}")

    expected_lines.sort()

    with open(manifest_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "Manifest contents do not match expected format, files, or sort order."

def test_clean_logs_redaction():
    clean_logs_dir = "/home/user/clean_logs"
    recovery_logs_dir = "/home/user/recovery/logs"

    assert os.path.isdir(clean_logs_dir), f"Directory {clean_logs_dir} is missing"

    # Check that all log files from recovery are present in clean_logs
    if os.path.isdir(recovery_logs_dir):
        for filename in os.listdir(recovery_logs_dir):
            if filename.endswith(".log"):
                clean_log_path = os.path.join(clean_logs_dir, filename)
                assert os.path.isfile(clean_log_path), f"Redacted log file {filename} missing in {clean_logs_dir}"

                with open(clean_log_path, "r") as f:
                    content = f.read()

                # Check that no IPv4 addresses remain
                ipv4_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
                found_ips = ipv4_pattern.findall(content)
                assert not found_ips, f"Found unredacted IP addresses in {filename}: {found_ips}"

                # Check that XXX.XXX.XXX.XXX is present (assuming original files had IPs)
                assert "XXX.XXX.XXX.XXX" in content, f"Expected redacted placeholder XXX.XXX.XXX.XXX not found in {filename}"

def test_tarball_contents():
    tarball_path = "/home/user/safe_backup.tar.gz"

    assert os.path.isfile(tarball_path), f"Tarball missing at {tarball_path}"

    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            members = tar.getnames()

            # Check for required files
            assert any(m.endswith("archive_manifest.txt") for m in members), "archive_manifest.txt missing from tarball"
            assert any(m.endswith("clean_logs/access.log") or m.endswith("clean_logs/system.log") for m in members), "clean_logs directory or its contents missing from tarball"

            # Check for forbidden files
            for m in members:
                assert "recovery" not in m, "Original recovery directory found in tarball"

            # Extract and check redacted content from tarball
            for member in tar.getmembers():
                if member.name.endswith(".log") and "clean_logs" in member.name:
                    f = tar.extractfile(member)
                    if f:
                        content = f.read().decode('utf-8')
                        ipv4_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
                        assert not ipv4_pattern.findall(content), f"Unredacted IP found in tarball log: {member.name}"
                        assert "XXX.XXX.XXX.XXX" in content, f"Redacted placeholder missing in tarball log: {member.name}"

    except tarfile.ReadError:
        pytest.fail(f"File at {tarball_path} is not a valid gzip-compressed tarball")