# test_final_state.py

import os
import json
import pytest

def test_check_policy_script_exists():
    script_path = "/home/user/check_policy.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_flagged_txt_correctness():
    flagged_path = "/home/user/flagged.txt"
    assert os.path.isfile(flagged_path), f"The output file {flagged_path} does not exist."

    metadata_path = "/home/user/metadata.json"
    assert os.path.isfile(metadata_path), f"The metadata file {metadata_path} is missing."

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    expected_flagged = []

    for item in metadata:
        filename = item.get("filename", "")
        original_path = item.get("original_path", "")
        csp_directive = item.get("csp_directive", "")

        flagged = False

        # Rule 1: Path Traversal
        if "../" in original_path:
            flagged = True

        # Rule 2: Binary Analysis
        file_path = os.path.join("/home/user/uploads", filename)
        if os.path.isfile(file_path):
            with open(file_path, "rb") as bf:
                content = bf.read()
                if content.startswith(b"\x7fELF") and b"malicious_payload_x86" in content:
                    flagged = True

        # Rule 3: CSP Enforcement
        if csp_directive != "strict-dynamic":
            flagged = True

        if flagged:
            expected_flagged.append(filename)

    expected_flagged.sort()

    with open(flagged_path, 'r') as f:
        actual_lines = f.read().splitlines()

    actual_flagged = [line.strip() for line in actual_lines if line.strip()]

    assert actual_flagged == expected_flagged, (
        f"The contents of {flagged_path} do not match the expected flagged files. "
        f"Expected: {expected_flagged}, Actual: {actual_flagged}"
    )