# test_final_state.py
import os
import json
import tarfile
import pytest

TAR_PATH = "/home/user/final_archive.tar.xz"
CURATED_DIR = "/home/user/curated_artifacts"
REGISTRY_PATH = "/home/user/registry.json"

def test_final_archive_exists():
    assert os.path.exists(TAR_PATH), f"Final archive missing at {TAR_PATH}"
    assert os.path.isfile(TAR_PATH), f"Path {TAR_PATH} is not a file"

def test_zip_slip_prevented():
    assert not os.path.exists("/home/user/pwned.txt"), "Zip slip payload was extracted to /home/user/pwned.txt!"
    assert not os.path.exists("/pwned.txt"), "Zip slip payload was extracted to /pwned.txt!"

def test_final_archive_size():
    assert os.path.exists(TAR_PATH), f"Final archive missing at {TAR_PATH}"
    size = os.path.getsize(TAR_PATH)
    threshold = 1500
    assert size <= threshold, f"Archive size {size} bytes exceeds maximum threshold of {threshold} bytes. Extreme compression (e.g., xz -9) is required."

def test_curated_artifacts_contents():
    assert os.path.exists(CURATED_DIR), f"Curated directory missing at {CURATED_DIR}"
    assert os.path.isdir(CURATED_DIR), f"Path {CURATED_DIR} is not a directory"

    files_in_curated = set()
    for root, _, files in os.walk(CURATED_DIR):
        for file in files:
            files_in_curated.add(file)
            assert not file.endswith(".dll"), f"Banned file {file} was extracted into curated directory."
            assert file != "pwned.txt", "Zip slip payload found in curated directory."

    expected_files = {"safe_bin1.exe", "safe_bin2.exe", "safe_bin3.exe"}
    assert files_in_curated == expected_files, f"Curated directory contents mismatch. Expected {expected_files}, got {files_in_curated}"

def test_registry_json_contents():
    assert os.path.exists(REGISTRY_PATH), f"Registry missing at {REGISTRY_PATH}"
    with open(REGISTRY_PATH, 'r') as f:
        try:
            registry = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("registry.json is not valid JSON")

    assert isinstance(registry, list), "Registry should be a JSON array"

    expected_files = {"safe_bin1.exe", "safe_bin2.exe", "safe_bin3.exe"}
    actual_files = set(os.path.basename(p) for p in registry)

    assert actual_files == expected_files, f"Registry contents mismatch. Expected {expected_files}, got {actual_files}"

    for p in registry:
        assert not p.endswith(".dll"), f"Banned file extension found in registry: {p}"
        assert "pwned.txt" not in p, f"Zip slip payload found in registry: {p}"

def test_tarball_contents():
    assert os.path.exists(TAR_PATH), f"Final archive missing at {TAR_PATH}"
    try:
        with tarfile.open(TAR_PATH, "r:xz") as tar:
            names = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"{TAR_PATH} is not a valid xz-compressed tar file")

    basenames = set(os.path.basename(name) for name in names if os.path.basename(name))

    expected_basenames = {"safe_bin1.exe", "safe_bin2.exe", "safe_bin3.exe", "registry.json"}

    for expected in expected_basenames:
        assert expected in basenames, f"Expected file {expected} missing from tarball"

    for name in basenames:
        assert not name.endswith(".dll"), f"Banned file extension found in tarball: {name}"
        assert name != "pwned.txt", "Zip slip payload found in tarball"