# test_final_state.py

import os
import tarfile
import tempfile
import pytest

def test_script_exists_and_uses_rename():
    script_path = "/home/user/process_artifacts.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "rename(" in content or "replace(" in content, "Script does not appear to use atomic rename (e.g. os.rename, Path.rename) as required."

def test_release_archive_exists():
    archive_path = "/home/user/outgoing/release.tar.gz"
    assert os.path.isfile(archive_path), f"Output archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"Output file {archive_path} is not a valid tar archive."

def test_release_archive_contents():
    archive_path = "/home/user/outgoing/release.tar.gz"

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall(path=tmpdir)

        metadata_path = os.path.join(tmpdir, "release", "metadata.txt")
        assert os.path.isfile(metadata_path), "release/metadata.txt is missing from the archive."
        with open(metadata_path, 'r') as f:
            metadata_content = f.read()
        expected_metadata = "Release Version: 2.4.1\nDate: 2023-10-15\nTarget: production\n"
        assert metadata_content == expected_metadata, f"metadata.txt content is incorrect. Got:\n{metadata_content}"

        bin_meta_path = os.path.join(tmpdir, "release", "artifacts", "bin1.meta")
        assert os.path.isfile(bin_meta_path), "release/artifacts/bin1.meta is missing from the archive."
        with open(bin_meta_path, 'r') as f:
            bin_meta_content = f.read()
        expected_bin_meta = "Binary: bin1\nVersion: 2.4.1\nEnv: production\n"
        assert bin_meta_content == expected_bin_meta, f"bin1.meta content is incorrect. Got:\n{bin_meta_content}"

        bin_dat_path = os.path.join(tmpdir, "release", "artifacts", "bin1.dat")
        assert os.path.isfile(bin_dat_path), "release/artifacts/bin1.dat is missing from the archive."
        with open(bin_dat_path, 'rb') as f:
            bin_dat_content = f.read()
        expected_bin_dat = b'\x00\x01\x02\x03\x04'
        assert bin_dat_content == expected_bin_dat, f"bin1.dat content is corrupted. Expected {expected_bin_dat}, got {bin_dat_content}"