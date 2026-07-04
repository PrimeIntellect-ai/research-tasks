# test_final_state.py
import os
import re

def test_cleaned_payload():
    path = "/home/user/cleaned_payload.txt"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Derive expected from worker.dmp
    dump_path = "/home/user/worker.dmp"
    assert os.path.isfile(dump_path), f"Dump file {dump_path} is missing."

    with open(dump_path, "rb") as f:
        dump_data = f.read()

    marker = b"CRIT_PAYLOAD_START:"
    idx = dump_data.find(marker)
    assert idx != -1, "Marker not found in dump."

    payload_start = dump_data[idx + len(marker):]
    space_idx = payload_start.find(b" ")
    assert space_idx != -1, "Space not found after marker in dump."

    raw_payload = payload_start[:space_idx].decode("ascii", errors="ignore")
    expected_cleaned = re.sub(r'[^0-9a-fA-F]', '', raw_payload)

    assert content == expected_cleaned, f"Contents of {path} do not match the expected cleaned payload. Expected '{expected_cleaned}', got '{content}'."

def test_crash_chunk():
    path = "/home/user/crash_chunk.txt"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    expected_chunk = "deadbeef"
    assert content.lower() == expected_chunk, f"Contents of {path} do not match the expected crash chunk. Expected '{expected_chunk}', got '{content}'."