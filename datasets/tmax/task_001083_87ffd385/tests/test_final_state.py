# test_final_state.py

import os
import struct
import pytest
import hashlib

def get_expected_files(base_dir):
    expected_files = {}
    for root, dirs, files in os.walk(base_dir, followlinks=False):
        # Prevent infinite loops in python walk just in case
        if os.path.islink(root):
            continue
        for f in files:
            full_path = os.path.join(root, f)
            if os.path.isfile(full_path) and not os.path.islink(full_path):
                rel_path = os.path.relpath(full_path, base_dir)
                with open(full_path, 'rb') as fp:
                    content = fp.read()
                expected_files[rel_path] = content
    return expected_files

def parse_archive(archive_path):
    if not os.path.exists(archive_path):
        return {}

    files_data = {}
    with open(archive_path, 'rb') as f:
        while True:
            magic = f.read(4)
            if not magic:
                break
            if magic != b'\xde\xad\xbe\xef':
                # Malformed archive
                raise ValueError("Invalid magic bytes found in archive.")

            path_len_data = f.read(2)
            if len(path_len_data) < 2:
                break
            path_len = struct.unpack('>H', path_len_data)[0]

            path_bytes = f.read(path_len)
            if len(path_bytes) < path_len:
                break
            path = path_bytes.decode('utf-8', errors='replace')

            chunk_idx_data = f.read(4)
            if len(chunk_idx_data) < 4:
                break
            chunk_idx = struct.unpack('>I', chunk_idx_data)[0]

            data_len_data = f.read(4)
            if len(data_len_data) < 4:
                break
            data_len = struct.unpack('>I', data_len_data)[0]

            payload = f.read(data_len)
            if len(payload) < data_len:
                break

            if path not in files_data:
                files_data[path] = {}
            files_data[path][chunk_idx] = payload

    # Reconstruct files
    reconstructed = {}
    for path, chunks in files_data.items():
        # Check if chunks are contiguous from 0 to N
        if not chunks:
            continue
        max_chunk = max(chunks.keys())
        if set(chunks.keys()) != set(range(max_chunk + 1)):
            # Missing chunks, cannot reconstruct
            continue

        file_content = b''.join(chunks[i] for i in range(max_chunk + 1))
        reconstructed[path] = file_content

    return reconstructed

def test_archive_f1_score():
    base_dir = "/home/user/artifacts"
    archive_path = "/home/user/repository.bin"

    assert os.path.exists(archive_path), f"Archive file {archive_path} does not exist."

    expected_files = get_expected_files(base_dir)

    try:
        archived_files = parse_archive(archive_path)
    except ValueError as e:
        pytest.fail(f"Failed to parse archive: {e}")

    correctly_archived = 0
    for path, content in archived_files.items():
        # Match by filename (ignoring leading slashes or dot-slashes)
        # Find corresponding expected file
        matched = False
        for exp_path, exp_content in expected_files.items():
            if exp_path == path or exp_path.endswith(path) or path.endswith(exp_path):
                if content == exp_content:
                    correctly_archived += 1
                    matched = True
                    break

    total_expected = len(expected_files)
    total_archived = len(archived_files)

    if total_archived == 0:
        precision = 0.0
    else:
        precision = correctly_archived / total_archived

    if total_expected == 0:
        recall = 1.0 if total_archived == 0 else 0.0
    else:
        recall = correctly_archived / total_expected

    if precision + recall == 0:
        f1_score = 0.0
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)

    assert f1_score >= 1.0, f"F1 score is {f1_score}, expected >= 1.0. Precision: {precision}, Recall: {recall}. Correct: {correctly_archived}, Expected: {total_expected}, Archived: {total_archived}."