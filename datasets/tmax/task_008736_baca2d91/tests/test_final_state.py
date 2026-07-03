# test_final_state.py

import os
import struct
import pytest

def get_config():
    config_path = '/home/user/chunk_config.ini'
    assert os.path.exists(config_path), f"Config file missing at {config_path}"

    config = {}
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                k, v = line.split('=', 1)
                config[k.strip()] = v.strip()

    assert 'max_chunk_size' in config, "max_chunk_size missing from config"
    assert 'output_dir' in config, "output_dir missing from config"

    return int(config['max_chunk_size']), config['output_dir']

def get_records():
    dump_path = '/home/user/project_dump.bin'
    assert os.path.exists(dump_path), f"Binary dump missing at {dump_path}"

    records = []
    with open(dump_path, 'rb') as f:
        while True:
            length_bytes = f.read(4)
            if not length_bytes:
                break
            assert len(length_bytes) == 4, "Incomplete length prefix in binary dump"
            length = struct.unpack('<I', length_bytes)[0]

            data = f.read(length)
            assert len(data) == length, "Incomplete record data in binary dump"

            text = data.decode('utf-16le')
            utf8_data = text.encode('utf-8')
            records.append(utf8_data)

    return records

def test_final_state():
    max_chunk_size, output_dir = get_config()
    records = get_records()

    expected_chunks = []
    current_chunk_records = []
    current_chunk_size = 0

    for rec in records:
        rec_len = len(rec)
        if current_chunk_size + rec_len > max_chunk_size and current_chunk_records:
            expected_chunks.append(current_chunk_records)
            current_chunk_records = [rec]
            current_chunk_size = rec_len
        else:
            current_chunk_records.append(rec)
            current_chunk_size += rec_len

    if current_chunk_records:
        expected_chunks.append(current_chunk_records)

    assert os.path.isdir(output_dir), f"Output directory missing: {output_dir}"

    expected_index_lines = []

    for i, chunk_records in enumerate(expected_chunks, start=1):
        chunk_filename = f"chunk_{i:03d}.log"
        chunk_path = os.path.join(output_dir, chunk_filename)

        assert os.path.exists(chunk_path), f"Expected chunk file missing: {chunk_path}"

        with open(chunk_path, 'rb') as f:
            actual_data = f.read()

        expected_data = b''.join(chunk_records)
        assert actual_data == expected_data, f"Content mismatch in {chunk_filename}"

        expected_index_lines.append(f"{chunk_filename},{len(chunk_records)}")

    # Check index.txt
    index_path = os.path.join(output_dir, 'index.txt')
    assert os.path.exists(index_path), f"Index file missing: {index_path}"

    with open(index_path, 'r') as f:
        actual_index_lines = [line.strip() for line in f if line.strip()]

    assert actual_index_lines == expected_index_lines, f"Index file content mismatch. Expected {expected_index_lines}, got {actual_index_lines}"

    # Check for unexpected chunk files
    actual_files = set(os.listdir(output_dir))
    expected_files = {f"chunk_{i:03d}.log" for i in range(1, len(expected_chunks) + 1)}
    expected_files.add("index.txt")

    unexpected_files = actual_files - expected_files
    assert not unexpected_files, f"Found unexpected files in output directory: {unexpected_files}"