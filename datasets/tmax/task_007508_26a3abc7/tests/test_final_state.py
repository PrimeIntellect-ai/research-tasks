# test_final_state.py

import os
import json
import tarfile
import hashlib
import pytest

def test_curate_script_exists():
    script_path = '/home/user/curate.py'
    assert os.path.isfile(script_path), f"{script_path} does not exist. The script must be created."

def test_manifest_json():
    manifest_path = '/home/user/manifest.json'
    assert os.path.isfile(manifest_path), f"{manifest_path} does not exist. The manifest file was not generated."

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{manifest_path} does not contain valid JSON.")

    # Recompute hashes from the known raw binary content to ensure correctness
    def get_sha256(content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    expected_manifest = {
        "app-1.0.bin": get_sha256("success_data_1"),
        "app-2.0.bin": get_sha256("success_data_2")
    }

    assert manifest == expected_manifest, f"The contents of {manifest_path} do not match the expected successful artifacts and hashes. Got: {manifest}"

def test_tarball_contents():
    tar_path = '/home/user/curated_repo.tar'
    assert os.path.isfile(tar_path), f"{tar_path} does not exist. The tar archive was not created."

    try:
        with tarfile.open(tar_path, 'r') as tar:
            members = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"{tar_path} is not a valid tar archive.")

    expected_members = {"app-1.0.bin", "app-2.0.bin"}
    actual_members = set(members)

    assert actual_members == expected_members, (
        f"Tarball contents are incorrect. Expected exactly {expected_members}, "
        f"but got {actual_members}. Ensure no parent directories are included and failed artifacts are omitted."
    )