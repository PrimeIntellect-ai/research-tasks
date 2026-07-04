# test_final_state.py

import os
import json
import tarfile
import subprocess
import pytest

def get_elf_machine(filepath):
    """Helper to get the Machine string from an ELF file using readelf."""
    try:
        output = subprocess.check_output(['readelf', '-h', filepath], universal_newlines=True)
        for line in output.splitlines():
            if 'Machine:' in line:
                return line.split('Machine:')[1].strip()
    except Exception:
        pass
    return None

def test_repo_directory_exists():
    """Test that the incoming backup was extracted to /home/user/repo."""
    repo_dir = "/home/user/repo"
    assert os.path.exists(repo_dir), f"Directory {repo_dir} does not exist."
    assert os.path.isdir(repo_dir), f"{repo_dir} is not a directory."
    assert os.path.exists(os.path.join(repo_dir, "app1")), "app1 is missing from the extracted repo."
    assert os.path.exists(os.path.join(repo_dir, "app2")), "app2 is missing from the extracted repo."

def test_elf_catalog_json():
    """Test that elf_catalog.json is correct."""
    catalog_path = "/home/user/elf_catalog.json"
    assert os.path.exists(catalog_path), f"{catalog_path} does not exist."

    with open(catalog_path, 'r') as f:
        try:
            catalog = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{catalog_path} is not a valid JSON file.")

    assert isinstance(catalog, dict), "The JSON file must contain a single dictionary."

    expected_keys = {"/home/user/repo/app1", "/home/user/repo/app2"}
    assert set(catalog.keys()) == expected_keys, f"Catalog keys must be exactly {expected_keys}."

    machine_app1 = get_elf_machine("/home/user/repo/app1")
    machine_app2 = get_elf_machine("/home/user/repo/app2")

    assert machine_app1 is not None, "Could not determine Machine type for app1."
    assert machine_app2 is not None, "Could not determine Machine type for app2."

    assert catalog["/home/user/repo/app1"] == machine_app1, "Incorrect Machine type for app1."
    assert catalog["/home/user/repo/app2"] == machine_app2, "Incorrect Machine type for app2."

def test_clean_artifacts_archive():
    """Test that clean_artifacts.tar.gz contains exactly app1 and app2 at the root."""
    archive_path = "/home/user/clean_artifacts.tar.gz"
    assert os.path.exists(archive_path), f"{archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()

    expected_members = {"app1", "app2"}
    assert set(members) == expected_members, f"Archive must contain exactly {expected_members} at the root, but contains {members}."

    with tarfile.open(archive_path, "r:gz") as tar:
        for member in tar.getmembers():
            assert member.isfile(), f"Archive member {member.name} is not a regular file."