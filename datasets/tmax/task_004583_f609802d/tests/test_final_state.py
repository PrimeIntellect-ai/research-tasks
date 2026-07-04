# test_final_state.py
import os
import pytest

def test_corrupt_list():
    corrupt_file = "/home/user/corrupt.list"
    assert os.path.exists(corrupt_file), f"File {corrupt_file} does not exist. The script should have generated it."

    with open(corrupt_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_corrupt = {
        "/home/user/repo_raw/group_alpha/sub1/corrupt-app.tar.gz",
        "/home/user/repo_raw/group_beta/broken.tar.gz"
    }

    assert set(lines) == expected_corrupt, f"Contents of {corrupt_file} do not match expected corrupt archives. Found: {lines}"
    assert len(lines) == len(expected_corrupt), f"{corrupt_file} has duplicate or extra lines."

def test_registry_csv():
    registry_file = "/home/user/registry.csv"
    assert os.path.exists(registry_file), f"File {registry_file} does not exist. The script should have generated it."

    with open(registry_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_registry = {
        "/home/user/repo_raw/group_alpha/sub1/app-v1.tar.gz,core-infra,release",
        "/home/user/repo_raw/group_beta/data-sync.tar.gz,data-eng,production",
        "/home/user/repo_raw/group_beta/data-verify.tar.gz,security,staging"
    }

    assert set(lines) == expected_registry, f"Contents of {registry_file} do not match expected registry entries. Found: {lines}"
    assert len(lines) == len(expected_registry), f"{registry_file} has duplicate or extra lines."

def test_script_uses_flock():
    script_file = "/home/user/curate_artifacts.sh"
    assert os.path.exists(script_file), f"Script {script_file} does not exist."

    with open(script_file, "r") as f:
        content = f.read()

    assert "flock" in content, f"Script {script_file} must use 'flock' to ensure thread-safe appending."