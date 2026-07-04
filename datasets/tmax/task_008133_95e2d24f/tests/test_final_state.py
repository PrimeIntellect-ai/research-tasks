# test_final_state.py

import os
import hashlib
import gzip
import tarfile
import io
import pytest

def get_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

def test_script_exists_and_executable():
    script_path = "/home/user/artifact_ingest.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_uses_flock():
    script_path = "/home/user/artifact_ingest.sh"
    with open(script_path, 'r') as f:
        content = f.read()
    assert "flock" in content, "Script does not use 'flock' command for concurrency control."

def test_lock_file_exists():
    lock_path = "/home/user/repo/repo.lock"
    assert os.path.isfile(lock_path), f"Lock file {lock_path} does not exist."

def test_artifacts_ingested_and_valid():
    incoming_dir = "/home/user/incoming"
    repo_dir = "/home/user/repo"

    # We expect file1.bin through file5.bin to be processed
    for i in range(1, 6):
        filename = f"file{i}.bin"
        filepath = os.path.join(incoming_dir, filename)
        assert os.path.isfile(filepath), f"Expected input file {filepath} is missing."

        file_hash = get_sha256(filepath)
        artifact_dir = os.path.join(repo_dir, file_hash)
        assert os.path.isdir(artifact_dir), f"Artifact directory {artifact_dir} missing for {filename}."

        manifest_path = os.path.join(artifact_dir, "manifest.txt")
        assert os.path.isfile(manifest_path), f"Manifest missing in {artifact_dir}."

        with open(manifest_path, 'r') as f:
            manifest_lines = [line.strip() for line in f.readlines() if line.strip()]

        assert len(manifest_lines) >= 4, f"Manifest in {artifact_dir} is incomplete."
        assert manifest_lines[0] == f"Original: {filename}", f"Manifest Original line incorrect in {manifest_path}."
        assert manifest_lines[1] == f"Original-SHA256: {file_hash}", f"Manifest Original-SHA256 line incorrect in {manifest_path}."
        assert manifest_lines[2] == "Chunks:", f"Manifest Chunks header missing in {manifest_path}."

        chunks_in_dir = sorted([c for c in os.listdir(artifact_dir) if c.startswith("chunk_")])
        assert len(chunks_in_dir) > 0, f"No chunks found in {artifact_dir}."

        chunk_lines = manifest_lines[3:]
        assert len(chunk_lines) == len(chunks_in_dir), f"Manifest chunk count mismatch in {manifest_path}."

        chunk_data = b""
        for chunk_line, chunk_file in zip(chunk_lines, chunks_in_dir):
            chunk_path = os.path.join(artifact_dir, chunk_file)
            chunk_hash = get_sha256(chunk_path)
            assert chunk_line == f"{chunk_file} {chunk_hash}", f"Manifest chunk entry incorrect for {chunk_file}."

            with open(chunk_path, 'rb') as cf:
                chunk_data += cf.read()

        # Reassemble and verify integrity
        try:
            decompressed = gzip.decompress(chunk_data)
        except Exception as e:
            pytest.fail(f"Failed to decompress chunks for {filename}: {e}")

        try:
            with tarfile.open(fileobj=io.BytesIO(decompressed), mode="r") as tar:
                members = tar.getmembers()
                assert len(members) == 1, f"Tarball should contain exactly 1 file, found {len(members)}."
                assert members[0].name == filename, f"Tarball contains {members[0].name}, expected {filename}."

                extracted_f = tar.extractfile(members[0])
                extracted_data = extracted_f.read()

                extracted_hash = hashlib.sha256(extracted_data).hexdigest()
                assert extracted_hash == file_hash, f"Reassembled file hash does not match original for {filename}."
        except Exception as e:
            pytest.fail(f"Failed to read tarball for {filename}: {e}")