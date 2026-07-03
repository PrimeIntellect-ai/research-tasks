# test_final_state.py

import os
import json
import hashlib
import struct
import pytest

MANIFEST_PATH = "/home/user/manifest.jsonl"
DATASET_DIR = "/home/user/dataset"

def test_manifest_exists():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist."

def test_manifest_contents_and_correctness():
    with open(MANIFEST_PATH, "r") as f:
        lines = [json.loads(l) for l in f if l.strip()]

    assert len(lines) == 6, f"Expected exactly 6 lines in manifest, got {len(lines)}."

    def get_entry(filepath):
        for l in lines:
            if l.get("filepath") == filepath:
                return l
        return None

    files_found = 0
    for root, _, files in os.walk(DATASET_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            if not (file.endswith(".gcode") or file.endswith(".elf") or file.endswith(".wal")):
                continue

            files_found += 1
            entry = get_entry(filepath)
            assert entry is not None, f"Missing manifest entry for {filepath}"

            # Check SHA256
            with open(filepath, "rb") as f_data:
                file_data = f_data.read()
                expected_sha256 = hashlib.sha256(file_data).hexdigest()
            assert entry.get("sha256") == expected_sha256, f"SHA256 mismatch for {filepath}"

            meta = entry.get("meta", {})
            assert isinstance(meta, dict), f"'meta' should be a dictionary for {filepath}"

            if file.endswith(".gcode"):
                assert entry.get("type") == "gcode", f"Expected type 'gcode' for {filepath}"
                # Compute expected max_z
                max_z = None
                with open(filepath, "r") as f_gcode:
                    for line in f_gcode:
                        if line.startswith("G0") or line.startswith("G1"):
                            parts = line.split()
                            for p in parts:
                                if p.startswith("Z"):
                                    try:
                                        z_val = float(p[1:])
                                        if max_z is None or z_val > max_z:
                                            max_z = z_val
                                    except ValueError:
                                        pass
                assert "max_z" in meta, f"Missing 'max_z' in meta for {filepath}"
                assert meta["max_z"] == max_z, f"max_z mismatch for {filepath}. Expected {max_z}, got {meta['max_z']}"

            elif file.endswith(".wal"):
                assert entry.get("type") == "wal", f"Expected type 'wal' for {filepath}"
                # Compute expected frames
                with open(filepath, "rb") as f_wal:
                    header = f_wal.read(32)
                    if len(header) == 32:
                        page_size = struct.unpack(">I", header[8:12])[0]
                        file_size = os.path.getsize(filepath)
                        frames = (file_size - 32) // (24 + page_size)
                    else:
                        frames = 0
                assert "frames" in meta, f"Missing 'frames' in meta for {filepath}"
                assert meta["frames"] == frames, f"frames mismatch for {filepath}. Expected {frames}, got {meta['frames']}"

            elif file.endswith(".elf"):
                assert entry.get("type") == "elf", f"Expected type 'elf' for {filepath}"
                assert "entry_point" in meta, f"Missing 'entry_point' in meta for {filepath}"
                assert isinstance(meta["entry_point"], int), f"'entry_point' must be an integer for {filepath}"

    assert files_found == 6, f"Expected to find 6 relevant files in {DATASET_DIR}, found {files_found}."