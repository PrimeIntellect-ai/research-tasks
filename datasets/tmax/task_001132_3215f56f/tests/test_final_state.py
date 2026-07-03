# test_final_state.py

import os
import base64
import hashlib

def test_valid_bins_manifest_exists_and_correct():
    export_file = "/home/user/export.txt"
    manifest_file = "/home/user/valid_bins.manifest"

    assert os.path.exists(export_file), f"Input file {export_file} is missing."
    assert os.path.exists(manifest_file), f"Output file {manifest_file} is missing."

    expected_lines = []

    with open(export_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = [p.strip() for p in line.split("|")]
            record_dict = {}
            for part in parts:
                if ":" in part:
                    key, val = part.split(":", 1)
                    record_dict[key.strip()] = val.strip()

            status = record_dict.get("STATUS", "")
            filename = record_dict.get("FILE", "")
            payload_b64 = record_dict.get("PAYLOAD", "")

            if status == "OK" and filename.endswith(".bin"):
                try:
                    raw_bytes = base64.b64decode(payload_b64)
                    file_hash = hashlib.sha256(raw_bytes).hexdigest()
                    expected_lines.append(f"{file_hash}  {filename}")
                except Exception as e:
                    pass

    expected_lines.sort()
    expected_content = "\n".join(expected_lines) + "\n"

    with open(manifest_file, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), (
        f"The content of {manifest_file} is incorrect.\n"
        f"Expected:\n{expected_content.strip()}\n\n"
        f"Actual:\n{actual_content.strip()}"
    )