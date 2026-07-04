# test_final_state.py

import os
import struct
import requests
import pytest
import shutil

def make_archive(path, key, entries):
    with open(path, 'wb') as f:
        f.write(b'BKP1')
        f.write(key.encode('ascii')[:8].ljust(8, b' '))
        for e_path, e_data in entries:
            path_bytes = e_path.encode('utf-8')
            f.write(struct.pack('<H', len(path_bytes)))
            f.write(path_bytes)
            f.write(struct.pack('<I', len(e_data)))
            f.write(e_data)

@pytest.fixture(scope="module")
def setup_archives(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("archives")

    good_archive = str(tmp_dir / "test1.bkp")
    bad_archive = str(tmp_dir / "test_badkey.bkp")

    make_archive(good_archive, 'Z9xQ2mP4', [
        ('valid/file1.txt', b'hello'),
        ('../escape.txt', b'bad1'),
        ('/absolute.txt', b'bad2'),
        ('deep/dir/file2.txt', b'world')
    ])

    make_archive(bad_archive, 'WRONGKEY', [
        ('valid/file.txt', b'data')
    ])

    return good_archive, bad_archive

def test_invalid_key(setup_archives, tmp_path):
    _, bad_archive = setup_archives
    target_dir = str(tmp_path / "restore_test2")

    try:
        resp = requests.post('http://127.0.0.1:8000/restore', json={
            "archive": bad_archive,
            "target": target_dir
        }, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the extraction service: {e}")

    assert resp.status_code == 403, f"Expected HTTP 403 for invalid key, got {resp.status_code}. Response: {resp.text}"

def test_valid_extraction_and_zip_slip(setup_archives, tmp_path):
    good_archive, _ = setup_archives
    target_dir = str(tmp_path / "restore_test")

    try:
        resp = requests.post('http://127.0.0.1:8000/restore', json={
            "archive": good_archive,
            "target": target_dir
        }, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the extraction service: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200 for valid extraction, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert data.get('extracted') == 2, f"Expected 2 extracted files, got {data.get('extracted')}"
    assert data.get('skipped') == 2, f"Expected 2 skipped files, got {data.get('skipped')}"

    # Check extracted files
    assert os.path.exists(os.path.join(target_dir, 'valid/file1.txt')), "Valid file 'valid/file1.txt' was not extracted."
    assert os.path.exists(os.path.join(target_dir, 'deep/dir/file2.txt')), "Valid file 'deep/dir/file2.txt' was not extracted."

    # Check malicious files were skipped
    parent_dir = os.path.dirname(target_dir)
    assert not os.path.exists(os.path.join(parent_dir, 'escape.txt')), "Zip Slip attack succeeded: '../escape.txt' was extracted."
    assert not os.path.exists('/absolute.txt'), "Zip Slip attack succeeded: '/absolute.txt' was extracted."