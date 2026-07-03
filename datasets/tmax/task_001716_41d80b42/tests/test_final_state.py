# test_final_state.py

import os
import json
import zipfile
import tarfile
import struct
import re
import pytest

DATASETS_DIR = '/home/user/datasets'
MALICIOUS_LOG = '/home/user/malicious.log'
REPORT_JSON = '/home/user/report.json'

def is_malicious_path(path):
    # Check for absolute paths or directory traversal
    if path.startswith('/'):
        return True
    parts = path.split('/')
    if '..' in parts:
        return True
    return False

def get_expected_results():
    malicious_files = set()
    report_data = {}

    for filename in os.listdir(DATASETS_DIR):
        filepath = os.path.join(DATASETS_DIR, filename)
        if not (filename.endswith('.zip') or filename.endswith('.tar.gz')):
            continue

        is_malicious = False
        archive_items = []

        if filename.endswith('.zip'):
            try:
                with zipfile.ZipFile(filepath, 'r') as z:
                    for info in z.infolist():
                        if is_malicious_path(info.filename):
                            is_malicious = True
                            break
                        archive_items.append((info.filename, z.read(info.filename)))
            except zipfile.BadZipFile:
                continue
        elif filename.endswith('.tar.gz'):
            try:
                with tarfile.open(filepath, 'r:gz') as t:
                    for info in t.getmembers():
                        if is_malicious_path(info.name):
                            is_malicious = True
                            break
                        f = t.extractfile(info)
                        if f is not None:
                            archive_items.append((info.name, f.read()))
            except tarfile.ReadError:
                continue

        if is_malicious:
            malicious_files.add(filename)
        else:
            report_data[filename] = {
                "gcode_totals": {},
                "elf_architectures": {}
            }
            for name, content in archive_items:
                if name.endswith('.gcode'):
                    total_e = 0.0
                    lines = content.decode('utf-8', errors='ignore').splitlines()
                    for line in lines:
                        if line.startswith('G1 '):
                            match = re.search(r'\bE([0-9.]+)', line)
                            if match:
                                total_e += float(match.group(1))
                    if total_e > 0 or any(line.startswith('G1 ') and 'E' in line for line in lines):
                        report_data[filename]["gcode_totals"][name] = round(total_e, 1)

                if content.startswith(b'\x7fELF'):
                    if len(content) >= 0x14:
                        e_machine = struct.unpack('<H', content[0x12:0x14])[0]
                        report_data[filename]["elf_architectures"][name] = e_machine

    return malicious_files, report_data

def test_malicious_log():
    assert os.path.isfile(MALICIOUS_LOG), f"{MALICIOUS_LOG} does not exist."

    expected_malicious, _ = get_expected_results()

    with open(MALICIOUS_LOG, 'r') as f:
        actual_malicious = set(line.strip() for line in f if line.strip())

    assert actual_malicious == expected_malicious, f"Expected malicious files {expected_malicious}, but found {actual_malicious} in {MALICIOUS_LOG}"

def test_report_json():
    assert os.path.isfile(REPORT_JSON), f"{REPORT_JSON} does not exist."

    _, expected_report = get_expected_results()

    with open(REPORT_JSON, 'r') as f:
        try:
            actual_report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_JSON} is not a valid JSON file.")

    assert actual_report == expected_report, f"Report JSON content mismatch. Expected: {expected_report}, Actual: {actual_report}"