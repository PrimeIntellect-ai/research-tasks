# test_final_state.py

import os
import tarfile
import pytest

def get_expected_paths():
    """Derive the expected relative paths based on the setup logic."""
    expected_paths = []
    for i in range(1, 101):
        year = 2020 + (i % 4)
        month = (i % 12) + 1
        expected_paths.append(f"{year}/{month:02d}/server_{i:03d}.conf")
    expected_paths.sort()
    return expected_paths

def test_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    script_path = "/home/user/migrate_configs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_migration_manifest():
    """Test that the migration manifest contains the correct sorted relative paths."""
    manifest_path = "/home/user/migration_manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest {manifest_path} does not exist."

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_paths = get_expected_paths()
    assert len(lines) == 100, f"Manifest should contain exactly 100 lines, found {len(lines)}."
    assert lines == expected_paths, "Manifest contents do not match the expected sorted paths."

def test_migrated_configs_archive():
    """Test that the migrated archive exists, contains correct paths, and files are updated."""
    archive_path = "/home/user/migrated_configs.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."

    expected_paths = get_expected_paths()

    with tarfile.open(archive_path, "r:gz") as tar:
        # Get all file members (ignoring directories)
        members = [m for m in tar.getmembers() if m.isfile()]
        member_names = sorted([m.name for m in members])

        assert member_names == expected_paths, "The paths inside the tar archive do not match the expected YYYY/MM/server_XXX.conf structure."

        # Check file contents for correct API_ENDPOINT replacement
        for member in members:
            f = tar.extractfile(member)
            content = f.read().decode('utf-8')

            assert "API_ENDPOINT=https://new.internal.corp/v2/api" in content, f"File {member.name} does not contain the updated API_ENDPOINT."
            assert "http://old.internal/api" not in content, f"File {member.name} still contains the old API_ENDPOINT."