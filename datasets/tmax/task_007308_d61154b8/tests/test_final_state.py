# test_final_state.py

import os
import json
import hashlib
import base64
import re
import pytest

def get_expected_report():
    valid_csp_file = "/home/user/valid_csp.txt"
    webroot_dir = "/home/user/webroot"

    # Read valid hashes
    valid_hashes = set()
    if os.path.exists(valid_csp_file):
        with open(valid_csp_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    valid_hashes.add(line)

    results = []

    # Walk through webroot
    for root, _, files in os.walk(webroot_dir):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)

                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract script contents
                # The task specifies exact tags <script> and </script>
                script_contents = re.findall(r'<script>(.*?)</script>', content, flags=re.DOTALL)

                unauthorized_hashes = set()
                for script in script_contents:
                    # Compute sha256 base64 hash
                    digest = hashlib.sha256(script.encode('utf-8')).digest()
                    b64_hash = base64.b64encode(digest).decode('utf-8')
                    full_hash = f"sha256-{b64_hash}"

                    if full_hash not in valid_hashes:
                        unauthorized_hashes.add(full_hash)

                if unauthorized_hashes:
                    # Get file permissions
                    stat_info = os.stat(filepath)
                    permissions = oct(stat_info.st_mode)[-4:]

                    results.append({
                        "file": filepath,
                        "unauthorized_hashes": sorted(list(unauthorized_hashes)),
                        "permissions": permissions
                    })

    # Sort results by file path
    results.sort(key=lambda x: x["file"])
    return results

def test_report_exists():
    assert os.path.isfile("/home/user/report.json"), "The file /home/user/report.json does not exist."

def test_report_content():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), "Cannot validate content because /home/user/report.json is missing."

    try:
        with open(report_path, "r", encoding="utf-8") as f:
            actual_report = json.load(f)
    except json.JSONDecodeError:
        pytest.fail("/home/user/report.json is not a valid JSON file.")

    expected_report = get_expected_report()

    # Check if actual report is a list
    assert isinstance(actual_report, list), "The JSON output must be an array of objects."

    # Check exact match
    assert len(actual_report) == len(expected_report), f"Expected {len(expected_report)} compromised files, but found {len(actual_report)}."

    for expected, actual in zip(expected_report, actual_report):
        assert actual.get("file") == expected["file"], f"Expected file path {expected['file']}, got {actual.get('file')}."
        assert actual.get("permissions") == expected["permissions"], f"Expected permissions {expected['permissions']} for {expected['file']}, got {actual.get('permissions')}."

        actual_hashes = actual.get("unauthorized_hashes", [])
        assert isinstance(actual_hashes, list), f"'unauthorized_hashes' for {expected['file']} must be an array."
        assert actual_hashes == expected["unauthorized_hashes"], f"Expected unauthorized hashes {expected['unauthorized_hashes']} for {expected['file']}, got {actual_hashes}."