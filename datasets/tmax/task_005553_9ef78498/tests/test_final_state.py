# test_final_state.py

import os
import stat
import base64
import gzip
import tarfile
import io
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/archive_optimizer.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_raw_directory_empty():
    raw_dir = "/home/user/backups/raw"
    assert os.path.isdir(raw_dir), f"Directory {raw_dir} does not exist."
    files = os.listdir(raw_dir)
    assert len(files) == 0, f"Raw directory {raw_dir} is not empty. Found: {files}"

def test_processed_files_exist():
    processed_dir = "/home/user/backups/processed"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} does not exist."

    expected_files = ["db_node_A.b64gz", "db_node_B.b64gz"]
    for f in expected_files:
        filepath = os.path.join(processed_dir, f)
        assert os.path.isfile(filepath), f"Expected processed file {filepath} does not exist."

def get_tar_contents_from_b64gz(filepath):
    with open(filepath, 'rb') as f:
        b64_data = f.read()

    try:
        gz_data = base64.b64decode(b64_data, validate=True)
    except Exception as e:
        pytest.fail(f"Failed to base64 decode {filepath}: {e}")

    try:
        tar_data = gzip.decompress(gz_data)
    except Exception as e:
        pytest.fail(f"Failed to gzip decompress {filepath}: {e}")

    try:
        with tarfile.open(fileobj=io.BytesIO(tar_data), mode='r') as tar:
            return tar.getnames()
    except Exception as e:
        pytest.fail(f"Failed to read tar archive from {filepath}: {e}")

def test_db_node_a_contents():
    filepath = "/home/user/backups/processed/db_node_A.b64gz"
    assert os.path.isfile(filepath), f"File {filepath} missing."

    names = get_tar_contents_from_b64gz(filepath)
    basenames = [os.path.basename(name) for name in names]

    assert "txn_10452.wal" in basenames, f"txn_10452.wal not found in {filepath}. Found: {basenames}"
    assert "dump1_64.elf" in basenames, f"dump1_64.elf not found in {filepath}. Found: {basenames}"

def test_db_node_b_contents():
    filepath = "/home/user/backups/processed/db_node_B.b64gz"
    assert os.path.isfile(filepath), f"File {filepath} missing."

    names = get_tar_contents_from_b64gz(filepath)
    basenames = [os.path.basename(name) for name in names]

    assert "txn_9912.wal" in basenames, f"txn_9912.wal not found in {filepath}. Found: {basenames}"
    assert "crash2_32.elf" in basenames, f"crash2_32.elf not found in {filepath}. Found: {basenames}"