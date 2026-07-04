# test_final_state.py

import os
import json
import stat
import hashlib
import re
import pytest

REPORT_PATH = "/home/user/forensics_report.json"
SUSPECT_DIR = "/home/user/suspect_dir"
IOC_HASHES_PATH = "/home/user/ioc_hashes.txt"

def get_expected_state():
    world_writable = []
    suid_sgid = []
    ioc_matches = []
    extracted_flags = set()

    # Read IOC hashes
    ioc_hashes = set()
    if os.path.exists(IOC_HASHES_PATH):
        with open(IOC_HASHES_PATH, 'r') as f:
            for line in f:
                h = line.strip()
                if h:
                    ioc_hashes.add(h)

    flag_pattern = re.compile(r"EVIDENCE_FLAG_[A-Z0-9]{16}")

    for root, _, files in os.walk(SUSPECT_DIR):
        for filename in files:
            filepath = os.path.join(root, filename)

            try:
                st = os.stat(filepath)
            except OSError:
                continue

            # Check world-writable
            if bool(st.st_mode & stat.S_IWOTH):
                world_writable.append(filepath)

            # Check SUID / SGID
            is_suid_sgid = bool(st.st_mode & (stat.S_ISUID | stat.S_ISGID))
            if is_suid_sgid:
                suid_sgid.append(filepath)

            # Check IOC match
            is_ioc_match = False
            try:
                with open(filepath, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                if file_hash in ioc_hashes:
                    ioc_matches.append(filepath)
                    is_ioc_match = True
            except OSError:
                pass

            # Extract flags if applicable
            if is_suid_sgid or is_ioc_match:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        flags = flag_pattern.findall(content)
                        extracted_flags.update(flags)
                except OSError:
                    pass

    return {
        "world_writable_files": sorted(world_writable),
        "suid_sgid_files": sorted(suid_sgid),
        "ioc_matches": sorted(ioc_matches),
        "extracted_flags": sorted(list(extracted_flags))
    }

@pytest.fixture(scope="module")
def report_data():
    assert os.path.exists(REPORT_PATH), f"Report file not found at {REPORT_PATH}"
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {REPORT_PATH} is not valid JSON.")
    return data

@pytest.fixture(scope="module")
def expected_data():
    return get_expected_state()

def test_report_structure(report_data):
    expected_keys = {"world_writable_files", "suid_sgid_files", "ioc_matches", "extracted_flags"}
    actual_keys = set(report_data.keys())
    assert expected_keys.issubset(actual_keys), f"Report is missing keys: {expected_keys - actual_keys}"

def test_world_writable_files(report_data, expected_data):
    actual = report_data.get("world_writable_files", [])
    expected = expected_data["world_writable_files"]
    assert actual == expected, f"Expected world_writable_files to be {expected}, but got {actual}"

def test_suid_sgid_files(report_data, expected_data):
    actual = report_data.get("suid_sgid_files", [])
    expected = expected_data["suid_sgid_files"]
    assert actual == expected, f"Expected suid_sgid_files to be {expected}, but got {actual}"

def test_ioc_matches(report_data, expected_data):
    actual = report_data.get("ioc_matches", [])
    expected = expected_data["ioc_matches"]
    assert actual == expected, f"Expected ioc_matches to be {expected}, but got {actual}"

def test_extracted_flags(report_data, expected_data):
    actual = report_data.get("extracted_flags", [])
    expected = expected_data["extracted_flags"]
    assert actual == expected, f"Expected extracted_flags to be {expected}, but got {actual}"