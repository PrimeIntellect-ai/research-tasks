# test_final_state.py

import os
import base64
import re
import difflib
import stat
import pytest

def test_authorized_keys_permissions_and_content():
    target_file = "/home/user/authorized_keys"
    traffic_log = "/app/traffic.log"

    assert os.path.exists(target_file), f"Output file {target_file} does not exist."

    # Check permissions (must be 0600)
    file_stat = os.stat(target_file)
    perms = oct(file_stat.st_mode)[-3:]
    assert perms == "600", f"File permissions for {target_file} must be 600, got {perms}."

    # Derive the expected key from the traffic log
    assert os.path.exists(traffic_log), f"Missing {traffic_log} to derive the expected key."

    expected_key = None
    with open(traffic_log, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("PAYLOAD:"):
                b64_payload = line.split("PAYLOAD:")[1]
                try:
                    decoded = base64.b64decode(b64_payload).decode('utf-8', errors='ignore')
                    # The audio intercept says the key ends with XYZ7NQ==
                    if "XYZ7NQ==" in decoded:
                        # Redact the internal 10.x.x.x IP address
                        expected_key = re.sub(r'10\.\d+\.\d+\.\d+', '[REDACTED]', decoded).strip()
                        break
                except Exception:
                    continue

    assert expected_key is not None, "Could not derive the expected key from traffic.log."

    # Read the agent's output
    with open(target_file, "r") as f:
        content = f.read().strip()

    # Calculate similarity ratio (using difflib.SequenceMatcher as a standard library equivalent to Levenshtein ratio)
    ratio = difflib.SequenceMatcher(None, content, expected_key).ratio()

    assert ratio >= 0.95, (
        f"Metric: {ratio} < 0.95\n"
        f"The authorized_keys content does not match the expected output closely enough.\n"
        f"Expected (redacted): {expected_key}\n"
        f"Got: {content}"
    )