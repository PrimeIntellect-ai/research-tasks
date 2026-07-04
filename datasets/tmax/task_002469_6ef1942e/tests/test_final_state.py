# test_final_state.py

import os
import glob
import pytest

def test_archives_organized():
    corrupted_dir = "/app/project_files/corrupted/"
    extracted_dir = "/app/project_files/extracted/"

    corrupted_files = glob.glob(os.path.join(corrupted_dir, "*.tar.gz"))
    assert len(corrupted_files) == 2, f"Expected 2 corrupted archives in {corrupted_dir}, found {len(corrupted_files)}."

    # Check that there are extracted contents (at least 3 items, assuming 3 valid archives)
    extracted_items = os.listdir(extracted_dir)
    assert len(extracted_items) >= 3, f"Expected contents from 3 valid archives in {extracted_dir}, found {len(extracted_items)} items."

def test_filtered_log_content():
    log_path = "/app/project_files/logs/filtered_system.log"
    assert os.path.isfile(log_path), f"Filtered log file {log_path} is missing."

    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        pytest.fail(f"File {log_path} is not valid UTF-8 encoded.")

    blocks = content.strip().split('---')
    valid_blocks_count = 0
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        valid_blocks_count += 1

        # Find Duration
        duration_found = False
        for line in block.split('\n'):
            if line.startswith('Duration:'):
                duration_str = line.split(':')[1].strip().replace('ms', '')
                try:
                    duration = int(duration_str)
                    assert duration >= 4500, f"Found a log entry with duration {duration}ms, which is less than the threshold 4500ms."
                    duration_found = True
                except ValueError:
                    pytest.fail(f"Could not parse duration from line: {line}")
        assert duration_found, f"Duration field missing in block: {block}"

    assert valid_blocks_count > 0, "Filtered log file contains no valid log blocks."

def test_packer_c_exists():
    c_file = "/app/project_files/packer.c"
    assert os.path.isfile(c_file), f"C source file {c_file} is missing."

def test_optimized_bin_size():
    bin_file = "/app/project_files/optimized.bin"
    assert os.path.isfile(bin_file), f"Optimized binary file {bin_file} is missing."

    size = os.path.getsize(bin_file)
    threshold = 12000
    assert size < threshold, f"Optimized binary size is {size} bytes, which is not less than the threshold of {threshold} bytes."