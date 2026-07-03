# test_final_state.py

import os
import subprocess
import hashlib
import csv
import pytest

def get_elf_info(filepath):
    try:
        output = subprocess.check_output(['readelf', '-h', filepath], stderr=subprocess.DEVNULL).decode('utf-8')
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    machine = None
    type_str = None
    for line in output.splitlines():
        if "Machine:" in line:
            machine = line.split("Machine:")[1].strip()
        elif "Type:" in line:
            type_raw = line.split("Type:")[1].strip()
            if "EXEC" in type_raw:
                type_str = "EXEC"
            elif "DYN" in type_raw:
                type_str = "DYN"
            else:
                type_str = "UNKNOWN"

    if machine and type_str:
        return machine.replace(" ", "_"), type_str
    return None

def get_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

@pytest.fixture(scope="module")
def expected_data():
    incoming_dir = "/home/user/incoming"
    expected = {}
    if not os.path.exists(incoming_dir):
        return expected

    for filename in os.listdir(incoming_dir):
        filepath = os.path.join(incoming_dir, filename)
        if not os.path.isfile(filepath):
            continue

        elf_info = get_elf_info(filepath)
        if elf_info:
            arch, type_str = elf_info
            sha256 = get_sha256(filepath)
            expected[filename] = {
                'sha256': sha256,
                'arch': arch,
                'type': type_str,
                'original_filepath': filepath
            }
    return expected

def test_script_exists():
    script_path = "/home/user/curate.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_manifest_exists_and_correct(expected_data):
    manifest_path = "/home/user/repo/manifest.csv"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    actual_manifest = []
    with open(manifest_path, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                actual_manifest.append(row)

    expected_rows = []
    for filename, data in expected_data.items():
        expected_rows.append([data['sha256'], data['arch'], data['type'], filename])

    assert len(actual_manifest) == len(expected_rows), "Manifest does not contain the correct number of entries."

    actual_sorted = sorted(actual_manifest, key=lambda x: x[3] if len(x) > 3 else "")
    expected_sorted = sorted(expected_rows, key=lambda x: x[3])

    for actual_row, expected_row in zip(actual_sorted, expected_sorted):
        assert actual_row == expected_row, f"Manifest row mismatch. Expected: {expected_row}, Got: {actual_row}"

def test_organized_files(expected_data):
    repo_dir = "/home/user/repo"
    assert os.path.isdir(repo_dir), f"Repo directory {repo_dir} does not exist."

    for filename, data in expected_data.items():
        expected_path = os.path.join(repo_dir, data['arch'], data['type'], filename)
        assert os.path.isfile(expected_path), f"Expected organized file is missing: {expected_path}"

        # Verify it's exactly the same file contents
        copied_sha256 = get_sha256(expected_path)
        assert copied_sha256 == data['sha256'], f"File contents mismatch for {expected_path}"