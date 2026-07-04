# test_final_state.py

import os
import stat
import hashlib
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/organize.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_script_uses_flock():
    script_path = "/home/user/organize.sh"
    with open(script_path, "r") as f:
        content = f.read()

    assert "flock" in content, "The script does not seem to use 'flock'."
    assert "/tmp/project_organizer.lock" in content, "The script does not reference the correct lock file."

def test_organized_data_files():
    organized_dir = "/home/user/organized_data"
    assert os.path.isdir(organized_dir), f"Directory {organized_dir} does not exist."

    expected_files = {
        "GAMMA_v1.dat": "ID:GAMMA VER:1\nData for gamma 1\n",
        "GAMMA_v3.dat": "ID:GAMMA VER:3\nData for gamma 3\n",
        "OMEGA_v2.dat": "ID:OMEGA VER:2\nData for omega 2\n",
        "OMEGA_v10.dat": "ID:OMEGA VER:10\nData for omega 10\n"
    }

    actual_files = set(os.listdir(organized_dir))
    assert actual_files == set(expected_files.keys()), f"Expected files in {organized_dir} to be {list(expected_files.keys())}, but found {list(actual_files)}."

    for filename, expected_content in expected_files.items():
        file_path = os.path.join(organized_dir, filename)
        with open(file_path, "r") as f:
            content = f.read()
        assert content == expected_content, f"Content of {filename} is incorrect."

def test_latest_data_symlinks():
    latest_dir = "/home/user/latest_data"
    assert os.path.isdir(latest_dir), f"Directory {latest_dir} does not exist."

    expected_links = {
        "GAMMA_latest.dat": "GAMMA_v3.dat",
        "OMEGA_latest.dat": "OMEGA_v10.dat"
    }

    actual_links = set(os.listdir(latest_dir))
    assert actual_links == set(expected_links.keys()), f"Expected symlinks in {latest_dir} to be {list(expected_links.keys())}, but found {list(actual_links)}."

    for link_name, target_name in expected_links.items():
        link_path = os.path.join(latest_dir, link_name)
        assert os.path.islink(link_path), f"{link_path} is not a symlink."

        target_path = os.readlink(link_path)
        # Target could be absolute or relative, resolve it
        if not os.path.isabs(target_path):
            target_path = os.path.normpath(os.path.join(latest_dir, target_path))

        expected_target_path = os.path.join("/home/user/organized_data", target_name)
        assert target_path == expected_target_path, f"Symlink {link_name} points to {target_path} instead of {expected_target_path}."

def test_manifest_checksums():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    organized_dir = "/home/user/organized_data"
    expected_checksums = {}
    for filename in ["GAMMA_v1.dat", "GAMMA_v3.dat", "OMEGA_v2.dat", "OMEGA_v10.dat"]:
        file_path = os.path.join(organized_dir, filename)
        with open(file_path, "rb") as f:
            expected_checksums[filename] = hashlib.sha256(f.read()).hexdigest()

    with open(manifest_path, "r") as f:
        manifest_lines = f.read().strip().splitlines()

    assert len(manifest_lines) == len(expected_checksums), "Manifest does not contain the correct number of entries."

    parsed_manifest = {}
    for line in manifest_lines:
        parts = line.split()
        assert len(parts) >= 2, f"Manifest line '{line}' is incorrectly formatted."
        checksum = parts[0]
        # Handle possible paths in manifest, standard sha256sum output usually has just filename if run correctly, but let's extract basename
        filename = os.path.basename(parts[1].lstrip('*'))
        parsed_manifest[filename] = checksum

    for filename, expected_checksum in expected_checksums.items():
        assert filename in parsed_manifest, f"{filename} is missing from the manifest."
        assert parsed_manifest[filename] == expected_checksum, f"Checksum for {filename} is incorrect in the manifest."

def test_project_inbox_cleanup():
    inbox_dir = "/home/user/project_inbox"
    assert os.path.isdir(inbox_dir), f"Directory {inbox_dir} does not exist."

    actual_files = set(os.listdir(inbox_dir))
    expected_files = {"readme.txt"}

    assert actual_files == expected_files, f"Expected {inbox_dir} to only contain {expected_files}, but found {actual_files}."