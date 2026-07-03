# test_final_state.py

import os
import tarfile
import hashlib

TAR_PATH = '/home/user/config_backup.tar.gz'
APP_CONFIGS_DIR = '/home/user/app_configs'
BACKUP_DIR = '/home/user/backup'
MANIFEST_PATH = '/home/user/backup/manifest.txt'
YAML_PATH = '/home/user/backup/consolidated.yaml'

def test_tarball_exists_and_valid():
    assert os.path.exists(TAR_PATH), f"Tarball not found at {TAR_PATH}"
    assert tarfile.is_tarfile(TAR_PATH), f"{TAR_PATH} is not a valid tar archive"

    with tarfile.open(TAR_PATH, 'r:gz') as tar:
        names = tar.getnames()

        # Check that both app_configs and backup contents are in the tarball
        # Paths inside tarball might be absolute or relative, so we check for substrings
        has_db_json = any('app_configs/db.json' in n for n in names)
        has_yaml = any('backup/consolidated.yaml' in n for n in names)

        assert has_db_json, "app_configs/db.json not found in the tarball"
        assert has_yaml, "backup/consolidated.yaml not found in the tarball"

def test_consolidated_yaml_content():
    assert os.path.exists(YAML_PATH), f"Consolidated YAML not found at {YAML_PATH}"

    with open(YAML_PATH, 'r') as f:
        content = f.read()

    # Since third-party libraries (like PyYAML) are restricted in this test suite,
    # we validate the presence of required structural keys and values as strings.
    assert 'db' in content, "Missing 'db' configuration section in YAML"
    assert 'server' in content, "Missing 'server' configuration section in YAML"
    assert 'metrics' in content, "Missing 'metrics' configuration section in YAML"

    assert 'admin_user' in content, "Missing database user 'admin_user' in YAML"
    assert '8080' in content, "Missing server port '8080' in YAML"
    assert '/metrics' in content, "Missing metrics endpoint '/metrics' in YAML"

def test_manifest_content_and_checksums():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file not found at {MANIFEST_PATH}"

    with open(MANIFEST_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Manifest should have exactly 4 lines, found {len(lines)}"

    filenames = []
    manifest_hashes = {}
    for line in lines:
        parts = line.split()
        assert len(parts) == 2, f"Invalid manifest line format (expected '<filename> <hash>'): '{line}'"
        fname, fhash = parts
        filenames.append(fname)
        manifest_hashes[fname] = fhash

    # Verify alphabetical sorting
    assert filenames == sorted(filenames), "Manifest lines are not sorted alphabetically by filename"

    expected_filenames = ['consolidated.yaml', 'db.json', 'metrics.xml', 'server.ini']
    assert filenames == expected_filenames, f"Manifest filenames mismatch. Expected {expected_filenames}, got {filenames}"

    # Verify checksums dynamically
    files_to_check = {
        'consolidated.yaml': YAML_PATH,
        'db.json': os.path.join(APP_CONFIGS_DIR, 'db.json'),
        'metrics.xml': os.path.join(APP_CONFIGS_DIR, 'metrics.xml'),
        'server.ini': os.path.join(APP_CONFIGS_DIR, 'server.ini')
    }

    for fname, filepath in files_to_check.items():
        assert os.path.exists(filepath), f"File {filepath} does not exist to verify checksum"

        with open(filepath, 'rb') as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()

        expected_hash = manifest_hashes[fname]
        assert actual_hash == expected_hash, f"Checksum mismatch for {fname}. Expected {actual_hash}, but manifest has {expected_hash}"