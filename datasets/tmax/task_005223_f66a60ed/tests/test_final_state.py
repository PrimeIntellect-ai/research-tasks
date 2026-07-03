# test_final_state.py

import os
import json
import re
import hashlib

def test_evasion_payload_generated_correctly():
    output_file = "/home/user/evasion_payload.txt"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    # 1. Derive expected username from logs
    auth_logs_path = "/home/user/auth_logs.log"
    assert os.path.exists(auth_logs_path), f"Missing {auth_logs_path}"

    target_user = None
    with open(auth_logs_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            log = json.loads(line)
            if log.get("status") == "blocked" and log.get("reason") == "SQLi_Attempt":
                target_user = log.get("username")
                break

    assert target_user is not None, "Could not find blocked SQLi_Attempt in auth_logs.log"

    # 2. Derive valid payloads that bypass the WAF
    threat_intel_path = "/home/user/threat_intel.json"
    waf_regex_path = "/home/user/waf_regex.txt"

    with open(threat_intel_path, "r") as f:
        payloads = json.load(f)

    with open(waf_regex_path, "r") as f:
        waf_regex_str = f.read().strip()

    waf_pattern = re.compile(waf_regex_str)

    valid_payloads = []
    for p in payloads:
        payload_str = p["payload"]
        if not waf_pattern.search(payload_str):
            valid_payloads.append(payload_str)

    # 3. Read the salt
    salt_path = "/home/user/salt.key"
    with open(salt_path, "r") as f:
        salt = f.read()

    # 4. Validate student output
    with open(output_file, "r") as f:
        student_output = f.read().strip()

    parts = student_output.split('|')
    assert len(parts) == 3, f"Output must contain exactly 3 parts separated by '|', got {len(parts)}"

    student_user, student_payload, student_hash = parts

    assert student_user == target_user, f"Expected username '{target_user}', got '{student_user}'"

    # The payload must bypass the WAF regex
    assert student_payload in valid_payloads, f"Payload '{student_payload}' either does not bypass the WAF regex or is not in the threat intel file."

    # Specifically check for the valid authentication bypass (OR condition equivalent)
    assert student_payload == "' || 1=1 #", f"Payload '{student_payload}' bypasses WAF but is not the correct universal authentication bypass payload."

    # Recompute and verify the hash
    expected_string = f"{student_user}:{student_payload}:{salt}"
    expected_hash = hashlib.sha256(expected_string.encode('utf-8')).hexdigest()

    assert student_hash == expected_hash, f"Expected SHA256 checksum {expected_hash}, got {student_hash}"