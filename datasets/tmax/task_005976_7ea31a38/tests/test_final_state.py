# test_final_state.py

import os
import hashlib
import re
import pytest

def test_go_file_exists():
    assert os.path.exists("/home/user/secops.go"), "/home/user/secops.go does not exist."
    assert os.path.isfile("/home/user/secops.go"), "/home/user/secops.go is not a file."

def test_clean_auth_logs_redacted():
    clean_logs_path = "/home/user/clean_auth_logs.txt"
    original_logs_path = "/home/user/auth_logs.txt"

    assert os.path.exists(clean_logs_path), f"{clean_logs_path} does not exist."

    with open(original_logs_path, 'r') as f:
        original_lines = f.read().splitlines()

    with open(clean_logs_path, 'r') as f:
        clean_lines = f.read().splitlines()

    assert len(original_lines) == len(clean_lines), "Cleaned logs line count does not match original logs."

    for orig, clean in zip(original_lines, clean_lines):
        parts_orig = orig.split(" | ")
        parts_clean = clean.split(" | ")

        assert len(parts_clean) == 4, f"Cleaned log line does not have 4 parts: {clean}"
        assert parts_clean[0] == parts_orig[0], "Timestamp was modified."
        assert parts_clean[1] == parts_orig[1], "IP address was modified."
        assert parts_clean[2] == parts_orig[2], "HTTP status was modified."
        assert parts_clean[3] == "[REDACTED_JWT]", f"JWT was not correctly redacted in line: {clean}"

def test_deny_policy_yaml():
    policy_path = "/home/user/deny_policy.yaml"
    assert os.path.exists(policy_path), f"{policy_path} does not exist."

    with open(policy_path, 'r') as f:
        content = f.read()

    # Check for required Kubernetes NetworkPolicy elements
    assert "kind: NetworkPolicy" in content, "Missing 'kind: NetworkPolicy' in yaml."
    assert "app: auth-service" in content, "Missing 'app: auth-service' label selector."
    assert "cidr: 0.0.0.0/0" in content, "Missing 'cidr: 0.0.0.0/0' in yaml."
    assert "except:" in content, "Missing 'except:' array in yaml."

    # Extract the except block items
    except_lines = []
    in_except = False
    for line in content.splitlines():
        line_stripped = line.strip()
        if line_stripped.startswith("except:"):
            in_except = True
            continue
        if in_except:
            if line_stripped.startswith("-"):
                ip = line_stripped.lstrip("- ").strip(" '\"")
                if ip:
                    except_lines.append(ip)
            elif line_stripped != "":
                # If we hit a non-empty line that doesn't start with '-', we might be out of the except block
                # assuming standard indentation, but this is a simple heuristic
                if not line.startswith(" ") and not line.startswith("\t"):
                    in_except = False

    expected_ips = ["198.51.100.22/32", "203.0.113.99/32"]

    # Check if expected IPs are in the extracted except list
    for ip in expected_ips:
        assert ip in except_lines, f"Malicious IP {ip} not found in the except block of {policy_path}."

    # Check if they are sorted alphabetically
    found_ips = [ip for ip in except_lines if ip in expected_ips]
    assert found_ips == sorted(found_ips), "The IPs in the except array are not sorted in ascending alphabetical order."

def test_checksum():
    clean_logs_path = "/home/user/clean_auth_logs.txt"
    checksum_path = "/home/user/checksum.txt"

    assert os.path.exists(checksum_path), f"{checksum_path} does not exist."

    with open(clean_logs_path, 'rb') as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    with open(checksum_path, 'r') as f:
        checksum_content = f.read().strip()

    # The checksum file should contain the hash and the filename
    assert actual_hash in checksum_content, f"The correct SHA256 hash ({actual_hash}) was not found in {checksum_path}."
    assert clean_logs_path in checksum_content, f"The file path {clean_logs_path} was not found in {checksum_path}."