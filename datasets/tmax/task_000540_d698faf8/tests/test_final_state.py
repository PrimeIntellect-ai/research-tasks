# test_final_state.py

import os
import glob
import pytest

def test_processed_files_exist_and_count():
    processed_dir = "/home/user/processed_data"
    files = sorted(os.listdir(processed_dir))

    # Filter out possible hidden files or unrelated files if any, 
    # but ideally the directory should only contain the chunks.
    chunk_files = [f for f in files if f.startswith("dataset_chunk_")]

    assert len(chunk_files) == 3, f"Expected exactly 3 chunk files, found {len(chunk_files)}: {chunk_files}"

def test_processed_files_content_and_encoding():
    processed_dir = "/home/user/processed_data"
    files = sorted([f for f in os.listdir(processed_dir) if f.startswith("dataset_chunk_")])

    assert len(files) == 3, "Need exactly 3 chunk files to test contents."

    all_lines = []

    for filename in files:
        filepath = os.path.join(processed_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            pytest.fail(f"File {filename} is not valid UTF-8.")

        assert len(lines) == 15, f"File {filename} should have exactly 15 lines, got {len(lines)}."
        all_lines.extend(lines)

    assert len(all_lines) == 45, f"Expected 45 total lines, got {len(all_lines)}."

    # The valid files are alpha.dat (20 lines, "café") and gamma.dat (25 lines, "façade")
    # They should be processed in alphabetical order: alpha.dat then gamma.dat.

    for i in range(20):
        assert "café" in all_lines[i], f"Line {i+1} expected to contain 'café', but got: {all_lines[i]}"

    for i in range(20, 45):
        assert "façade" in all_lines[i], f"Line {i+1} expected to contain 'façade', but got: {all_lines[i]}"