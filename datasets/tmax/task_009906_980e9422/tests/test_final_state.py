# test_final_state.py

import os
import base64
from collections import Counter

def test_malicious_ips_correct():
    log_path = "/home/user/gateway.log"
    output_path = "/home/user/malicious_ips.txt"

    assert os.path.exists(output_path), f"The output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"The path {output_path} is not a file."

    # Derive the expected malicious IPs from the log file
    assert os.path.exists(log_path), f"The log file {log_path} is missing."

    keys = []
    entries = []

    with open(log_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Example line: 203.0.113.1 - - [2024-10-12T10:01:01Z] "GET /api/v1/data HTTP/1.1" 200 - User: alice Token: c29tZXRva2Vu
            parts = line.split()
            ip = parts[0]
            timestamp = parts[3].strip('[]')
            user = parts[11]
            token = parts[13]

            plaintext = f"{timestamp}:{user}".encode('utf-8')
            try:
                decoded_token = base64.b64decode(token)
            except Exception:
                continue

            # Recover the key stream
            key_stream = bytes([b ^ k for b, k in zip(decoded_token, plaintext)])

            # The key is repeated, but we can just use the key stream as a signature for the key
            # Since plaintext length varies, let's just find the repeating pattern or just use the first few bytes
            # Actually, the key length is unknown, but we can assume the key stream prefix is consistent for the same key.
            # Let's just use the first 10 bytes of the key stream to identify the key.
            key_prefix = key_stream[:10]
            keys.append(key_prefix)
            entries.append((ip, key_prefix))

    # The most common key prefix is the legitimate one
    key_counts = Counter(keys)
    assert len(key_counts) > 0, "Could not extract any keys from the log file."
    legitimate_key_prefix = key_counts.most_common(1)[0][0]

    expected_malicious_ips = set()
    for ip, key_prefix in entries:
        if key_prefix != legitimate_key_prefix:
            expected_malicious_ips.add(ip)

    expected_sorted_ips = sorted(list(expected_malicious_ips))

    # Read the actual output
    with open(output_path, 'r') as f:
        actual_ips = [line.strip() for line in f if line.strip()]

    assert actual_ips == expected_sorted_ips, (
        f"The IPs in {output_path} do not match the expected malicious IPs.\n"
        f"Expected: {expected_sorted_ips}\n"
        f"Actual: {actual_ips}"
    )