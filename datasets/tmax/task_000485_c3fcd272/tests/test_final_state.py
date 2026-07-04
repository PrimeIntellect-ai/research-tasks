# test_final_state.py
import os
import struct
import pytest

def test_organized_dataset_symlinks():
    raw_dir = "/home/user/raw_dataset"
    organized_dir = "/home/user/organized_dataset"

    assert os.path.isdir(raw_dir), f"Directory {raw_dir} does not exist."
    assert os.path.isdir(organized_dir), f"Directory {organized_dir} does not exist."

    # Find all .dat files in the raw dataset
    raw_files = [f for f in os.listdir(raw_dir) if f.endswith('.dat')]
    assert len(raw_files) > 0, f"No .dat files found in {raw_dir}."

    expected_symlinks = {}

    for raw_file in raw_files:
        raw_path = os.path.join(raw_dir, raw_file)

        # Read the header to determine expected symlink location
        with open(raw_path, "rb") as f:
            header = f.read(24)

        assert len(header) == 24, f"File {raw_path} is smaller than 24 bytes."

        magic = header[0:8]
        if magic != b"SNSR_DAT":
            continue # Skip files that don't match the magic string if any

        sensor_id_raw = header[8:16]
        sensor_id = sensor_id_raw.replace(b'\x00', b'').decode('ascii')

        timestamp = struct.unpack("<Q", header[16:24])[0]

        expected_symlink_path = os.path.join(organized_dir, sensor_id, f"{timestamp}.dat")
        expected_symlinks[expected_symlink_path] = raw_path

    assert len(expected_symlinks) > 0, "No valid sensor data files were found to verify."

    # Verify each expected symlink
    for symlink_path, target_path in expected_symlinks.items():
        assert os.path.exists(symlink_path), f"Expected symlink is missing: {symlink_path}"
        assert os.path.islink(symlink_path), f"Path exists but is not a symlink: {symlink_path}"

        actual_target = os.readlink(symlink_path)
        assert actual_target == target_path, (
            f"Symlink {symlink_path} points to {actual_target}, "
            f"but should point to {target_path}"
        )

    # Verify no unexpected files exist in the organized directory
    actual_symlinks_found = 0
    for root, dirs, files in os.walk(organized_dir):
        for file in files:
            file_path = os.path.join(root, file)
            assert file_path in expected_symlinks, f"Unexpected file found in organized dataset: {file_path}"
            actual_symlinks_found += 1

    assert actual_symlinks_found == len(expected_symlinks), (
        f"Expected {len(expected_symlinks)} symlinks, but found {actual_symlinks_found}."
    )