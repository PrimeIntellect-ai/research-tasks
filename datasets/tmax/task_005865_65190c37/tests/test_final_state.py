# test_final_state.py

import os
import pytest

APPROVED_ARTIFACTS = ["auth-v1.bin", "cache-v4.bin", "core-v1.bin"]
UNAPPROVED_ARTIFACTS = ["db-v3.bin", "ui-v2.bin"]

def test_curate_script_exists_and_executable():
    script_path = "/home/user/curate.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_curation_summary_log():
    log_path = "/home/user/curation_summary.log"
    assert os.path.isfile(log_path), f"Summary log {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == APPROVED_ARTIFACTS, f"Summary log contents are incorrect. Expected {APPROVED_ARTIFACTS}, got {lines}"

def test_binaries_moved_correctly():
    repo_dir = "/home/user/repo/binaries"
    incoming_dir = "/home/user/incoming"

    for artifact in APPROVED_ARTIFACTS:
        repo_path = os.path.join(repo_dir, artifact)
        incoming_path = os.path.join(incoming_dir, artifact)
        assert os.path.isfile(repo_path), f"Approved artifact {artifact} was not moved to {repo_dir}."
        assert not os.path.isfile(incoming_path), f"Approved artifact {artifact} still exists in {incoming_dir}."

    for artifact in UNAPPROVED_ARTIFACTS:
        repo_path = os.path.join(repo_dir, artifact)
        incoming_path = os.path.join(incoming_dir, artifact)
        assert not os.path.isfile(repo_path), f"Unapproved artifact {artifact} should not be in {repo_dir}."
        assert os.path.isfile(incoming_path), f"Unapproved artifact {artifact} should still be in {incoming_dir}."

def test_manifest_updated_correctly():
    manifest_path = "/home/user/repo/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    with open(manifest_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    manifest_dict = {}
    for line in lines:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            manifest_dict[parts[0]] = parts[1]

    for artifact in APPROVED_ARTIFACTS:
        status = manifest_dict.get(artifact)
        assert status == "APPROVED", f"Artifact {artifact} status in manifest is '{status}', expected 'APPROVED'."

    for artifact in UNAPPROVED_ARTIFACTS:
        status = manifest_dict.get(artifact)
        assert status == "PENDING", f"Artifact {artifact} status in manifest is '{status}', expected 'PENDING'."

    assert manifest_dict.get("legacy-v1.bin") == "APPROVED", "legacy-v1.bin status was incorrectly modified."