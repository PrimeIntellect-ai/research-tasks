# test_final_state.py

import os
import tarfile
import pytest

def test_curated_artifacts_dir_exists():
    path = "/home/user/curated_artifacts"
    assert os.path.isdir(path), f"Directory does not exist: {path}"

def test_curated_artifacts_files():
    curated_dir = "/home/user/curated_artifacts"
    expected_files = {"alpha.tar.gz", "beta.tar.gz", "delta.tar.gz"}

    # Check that expected files are present
    for f in expected_files:
        path = os.path.join(curated_dir, f)
        assert os.path.isfile(path), f"Expected curated artifact missing: {path}"

    # Check that gamma.tar.gz is NOT present
    gamma_path = os.path.join(curated_dir, "gamma.tar.gz")
    assert not os.path.exists(gamma_path), f"gamma.tar.gz should have failed validation and not be curated"

def test_alpha_curated_content():
    path = "/home/user/curated_artifacts/alpha.tar.gz"
    assert os.path.isfile(path), f"File missing: {path}"

    with tarfile.open(path, "r:gz") as tar:
        names = tar.getnames()
        assert "metadata.txt" in names, "metadata.txt missing in alpha.tar.gz root"
        assert "payload.bin" in names, "payload.bin missing in alpha.tar.gz root"

        with tar.extractfile("metadata.txt") as f:
            metadata = f.read().decode('utf-8')
            assert "Version: v1.1.0" in metadata, "alpha metadata not correctly updated (Version)"
            assert "Source: https://secure-repo.local/bin" in metadata, "alpha metadata not correctly updated (Source)"

        with tar.extractfile("payload.bin") as f:
            payload = f.read().decode('utf-8')
            assert "binary_data_alpha" in payload, "alpha payload.bin content altered"

def test_beta_curated_content():
    path = "/home/user/curated_artifacts/beta.tar.gz"
    assert os.path.isfile(path), f"File missing: {path}"

    with tarfile.open(path, "r:gz") as tar:
        names = tar.getnames()
        assert "metadata.txt" in names, "metadata.txt missing in beta.tar.gz root"
        assert "payload.bin" in names, "payload.bin missing in beta.tar.gz root"

        with tar.extractfile("metadata.txt") as f:
            metadata = f.read().decode('utf-8')
            assert "Name: beta" in metadata, "beta metadata Name missing"
            assert "STATUS=PUBLISHED" in metadata, "beta metadata not correctly updated (STATUS)"

        with tar.extractfile("payload.bin") as f:
            payload = f.read().decode('utf-8')
            assert "binary_data_beta" in payload, "beta payload.bin content altered"

def test_delta_curated_content():
    path = "/home/user/curated_artifacts/delta.tar.gz"
    assert os.path.isfile(path), f"File missing: {path}"

    with tarfile.open(path, "r:gz") as tar:
        names = tar.getnames()
        assert "metadata.txt" in names, "metadata.txt missing in delta.tar.gz root"
        assert "payload.bin" in names, "payload.bin missing in delta.tar.gz root"

        with tar.extractfile("metadata.txt") as f:
            metadata = f.read().decode('utf-8')
            assert "Name: delta" in metadata, "delta metadata Name missing"
            assert "arch=amd64" in metadata, "delta metadata not correctly updated (arch)"

        with tar.extractfile("payload.bin") as f:
            payload = f.read().decode('utf-8')
            assert "binary_data_delta" in payload, "delta payload.bin content altered"

def test_curation_log():
    log_path = "/home/user/curation_log.txt"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "FAILED: gamma.tar.gz",
        "SUCCESS: alpha.tar.gz",
        "SUCCESS: beta.tar.gz",
        "SUCCESS: delta.tar.gz"
    ]

    assert lines == expected_lines, f"Log file content does not match expected alphabetically sorted output. Got: {lines}"