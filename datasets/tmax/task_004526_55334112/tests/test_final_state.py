# test_final_state.py

import os
import zipfile
import pytest

def test_malicious_log():
    log_path = '/home/user/artifacts/malicious.log'
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    expected_lines = sorted([
        '../escape1.bin',
        'configs/../../escape2.bin',
        '/absolute/path/escape3.bin'
    ])

    assert lines == expected_lines, f"Contents of {log_path} do not match the expected sorted malicious paths. Found: {lines}"

def test_raw_files_extracted_correctly():
    raw_dir = '/home/user/artifacts/raw'
    assert os.path.isdir(raw_dir), f"Directory {raw_dir} does not exist."

    expected_files = {
        'firmware_v1.bin.safe': b'\x00\x01\x02\x03',
        'settings.dat.safe': b'config_data=123',
        'logo.png.safe': b'PNG...'
    }

    actual_files = set(os.listdir(raw_dir))
    assert actual_files == set(expected_files.keys()), f"Files in {raw_dir} do not match expected. Found: {actual_files}"

    for filename, expected_content in expected_files.items():
        filepath = os.path.join(raw_dir, filename)
        with open(filepath, 'rb') as f:
            content = f.read()
        assert content == expected_content, f"Content of {filename} does not match expected."

def test_symlinks_created_correctly():
    links_dir = '/home/user/artifacts/links'
    assert os.path.isdir(links_dir), f"Directory {links_dir} does not exist."

    expected_links = ['firmware_v1.bin', 'settings.dat', 'logo.png']
    actual_links = set(os.listdir(links_dir))

    assert actual_links == set(expected_links), f"Symlinks in {links_dir} do not match expected. Found: {actual_links}"

    for link_name in expected_links:
        link_path = os.path.join(links_dir, link_name)
        assert os.path.islink(link_path), f"{link_path} is not a symbolic link."

        target = os.readlink(link_path)
        expected_target = f'/home/user/artifacts/raw/{link_name}.safe'
        assert target == expected_target, f"Symlink {link_path} points to {target}, expected {expected_target}."
        assert os.path.exists(link_path), f"Symlink {link_path} is broken (target does not exist)."