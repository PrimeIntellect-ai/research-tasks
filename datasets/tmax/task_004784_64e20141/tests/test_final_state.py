# test_final_state.py

import os
import subprocess
import tempfile
import hashlib
import pytest

def test_failure_count():
    """Check if the failure count is exactly 43."""
    count_file = "/home/user/failure_count.txt"
    assert os.path.isfile(count_file), f"Missing {count_file}"
    with open(count_file, "r") as f:
        content = f.read().strip()
    assert content == "43", f"Expected failure count 43, but got {content}"

def test_process_manifests_executable():
    """Check if the process_manifests script exists and is executable."""
    script_path = "/home/user/process_manifests"
    assert os.path.isfile(script_path), f"Missing script {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_process_manifests_clean_corpus():
    """Run process_manifests on the clean corpus and verify all files are processed correctly."""
    script_path = "/home/user/process_manifests"
    clean_in = "/app/corpus/clean"

    with tempfile.TemporaryDirectory() as clean_out:
        result = subprocess.run([script_path, clean_in, clean_out], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on clean corpus. stderr: {result.stderr}"

        expected_files = set(os.listdir(clean_in))
        actual_files = set(os.listdir(clean_out))

        # manifest.sha256 should be there
        assert "manifest.sha256" in actual_files, "manifest.sha256 is missing in clean output directory"
        actual_files.remove("manifest.sha256")

        missing = expected_files - actual_files
        assert not missing, f"Clean files missing from output: {missing}"

        # Verify UTF-8 encoding and SHA256 manifest
        manifest_path = os.path.join(clean_out, "manifest.sha256")
        with open(manifest_path, "r") as f:
            manifest_lines = f.read().strip().splitlines()

        manifest_hashes = {}
        for line in manifest_lines:
            if not line.strip():
                continue
            parts = line.split(None, 1)
            if len(parts) == 2:
                # Format: hash [ *]filename
                filename = parts[1].lstrip(" *")
                manifest_hashes[filename] = parts[0]

        for filename in expected_files:
            file_path = os.path.join(clean_out, filename)
            # Check UTF-8
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                pytest.fail(f"File {filename} is not valid UTF-8")

            # Check SHA256
            with open(file_path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            assert filename in manifest_hashes, f"File {filename} missing from manifest.sha256"
            assert manifest_hashes[filename] == file_hash, f"Hash mismatch for {filename} in manifest"

def test_process_manifests_evil_corpus():
    """Run process_manifests on the evil corpus and verify all files are rejected."""
    script_path = "/home/user/process_manifests"
    evil_in = "/app/corpus/evil"

    with tempfile.TemporaryDirectory() as evil_out:
        result = subprocess.run([script_path, evil_in, evil_out], capture_output=True, text=True)
        # Even if it returns non-zero, the requirement is that NO evil files are copied.

        expected_files = set(os.listdir(evil_in))
        actual_files = set(os.listdir(evil_out))

        if "manifest.sha256" in actual_files:
            actual_files.remove("manifest.sha256")

        bypassed = actual_files.intersection(expected_files)
        assert not bypassed, f"{len(bypassed)} of {len(expected_files)} evil bypassed: {bypassed}"

        # Ensure no other files were written
        assert not actual_files, f"Unexpected files in evil output directory: {actual_files}"