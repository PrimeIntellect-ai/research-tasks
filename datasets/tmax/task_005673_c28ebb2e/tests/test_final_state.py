# test_final_state.py

import os
import glob
import tarfile
import tempfile
import shutil

def test_final_backup_chunks_exist_and_sized_correctly():
    backup_dir = "/home/user/final_backup"
    chunk_pattern = os.path.join(backup_dir, "updated_configs.tar.gz.*")
    chunks = sorted(glob.glob(chunk_pattern))

    assert len(chunks) > 0, "No split archive chunks found in /home/user/final_backup/"

    # Check sizes
    for chunk in chunks[:-1]:
        size = os.path.getsize(chunk)
        assert size == 500, f"Chunk {chunk} is {size} bytes, expected exactly 500 bytes"

def test_reassembled_tarball_contents():
    backup_dir = "/home/user/final_backup"
    chunk_pattern = os.path.join(backup_dir, "updated_configs.tar.gz.*")
    chunks = sorted(glob.glob(chunk_pattern))

    assert len(chunks) > 0, "No split archive chunks found to reassemble."

    with tempfile.TemporaryDirectory() as temp_dir:
        merged_tar_path = os.path.join(temp_dir, "merged.tar.gz")

        # Reassemble
        with open(merged_tar_path, 'wb') as outfile:
            for chunk in chunks:
                with open(chunk, 'rb') as infile:
                    outfile.write(infile.read())

        # Extract and verify
        assert tarfile.is_tarfile(merged_tar_path), "Reassembled file is not a valid tar archive."

        extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_dir)

        with tarfile.open(merged_tar_path, 'r:gz') as tar:
            tar.extractall(path=extract_dir)

        extracted_files = os.listdir(extract_dir)

        expected_files = {"app1.conf", "app2.conf", "worker.conf", "dashboard.conf"}
        actual_files = set(extracted_files)

        assert expected_files.issubset(actual_files), f"Missing expected files in tarball. Found: {actual_files}"

        # Verify contents
        old_string = "db_host=old-db.legacy.local"
        new_string = "db_host=new-cluster.modern.local"

        new_string_count = 0

        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if file.endswith(".conf"):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r') as f:
                        content = f.read()
                        assert old_string not in content, f"Found old database string in {file}"
                        if new_string in content:
                            new_string_count += content.count(new_string)

        assert new_string_count == 4, f"Expected exactly 4 occurrences of the new database string, found {new_string_count}"