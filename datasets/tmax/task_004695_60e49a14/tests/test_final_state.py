# test_final_state.py
import os
import json
import gzip
import struct
import hashlib
import glob
import pytest

def get_expected_tuples():
    import walparser

    backups_dir = "/home/user/backups"
    wal_files = glob.glob(os.path.join(backups_dir, "*.wal.gz"))

    expected_tuples = set()
    for filepath in wal_files:
        # Compute SHA256 of compressed file
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            compressed_data = f.read()
            hasher.update(compressed_data)
        checksum = hasher.hexdigest()

        # Read timestamp from first 8 bytes of uncompressed data
        with gzip.open(filepath, 'rb') as f:
            timestamp_bytes = f.read(8)
            # Need to rewind for the parser
            f.seek(0)
            parsed_data = walparser.parse_stream(f)

        if len(timestamp_bytes) < 8:
            continue

        timestamp = struct.unpack('<q', timestamp_bytes)[0]
        expected_filename = f"state_{timestamp}.wal.gz"

        keys = set()
        for item in parsed_data:
            if 'key' in item:
                keys.add(item['key'])

        expected_tuples.add((expected_filename, checksum, tuple(sorted(keys))))

    return expected_tuples

def test_manifest_f1_score():
    manifest_path = "/home/user/manifest.json"
    assert os.path.exists(manifest_path), f"Manifest file not found at {manifest_path}"

    try:
        import walparser
    except ImportError:
        pytest.fail("walparser package is not installed. Agent failed to install it.")

    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Manifest file {manifest_path} is not valid JSON")

    expected_tuples = get_expected_tuples()
    assert len(expected_tuples) > 0, "No valid WAL files found to generate expected tuples"

    agent_tuples = set()
    for filename, data in manifest.items():
        if not isinstance(data, dict):
            continue
        checksum = data.get('checksum', '')
        keys = data.get('keys', [])
        agent_tuples.add((filename, checksum, tuple(sorted(keys))))

    true_positives = len(agent_tuples.intersection(expected_tuples))

    precision = true_positives / len(agent_tuples) if agent_tuples else 0.0
    recall = true_positives / len(expected_tuples) if expected_tuples else 0.0

    if precision + recall == 0:
        f1_score = 0.0
    else:
        f1_score = 2 * precision * recall / (precision + recall)

    assert f1_score >= 0.95, f"F1 score {f1_score:.4f} is below the threshold of 0.95. Precision: {precision:.4f}, Recall: {recall:.4f}"