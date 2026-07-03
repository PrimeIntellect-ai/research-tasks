# test_final_state.py
import os
import hashlib
import pytest

OUTPUT_FILE = "/home/user/unique_network_configs.txt"

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"The output file {OUTPUT_FILE} does not exist. Did the script run successfully?"
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a file."

def test_output_file_contents():
    # Expected key=value pairs based on the setup data
    expected_pairs = [
        "network.proxy.url=http://proxy.local:8080",
        "network.timeout=30",
        "network.dns.secondary=8.8.4.4",
        "network.dns.primary=8.8.8.8",
        "network.host.tags=region=east,env=prod"
    ]

    # Compute their md5 hashes and construct the expected lines
    expected_lines = []
    for pair in expected_pairs:
        md5_hash = hashlib.md5(pair.encode('utf-8')).hexdigest()
        expected_lines.append(f"{md5_hash}  {pair}")

    # The output must be sorted alphabetically by the MD5 hash
    expected_lines.sort()

    with open(OUTPUT_FILE, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in {OUTPUT_FILE}, but found {len(actual_lines)}. "
        "Make sure deduplication is working correctly."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} mismatch.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}\n"
            "Ensure the script correctly decodes unicode escapes, formats as '<hash>  key=value', and sorts by hash."
        )