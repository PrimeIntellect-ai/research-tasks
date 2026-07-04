# test_final_state.py

import os
import json
import hashlib
import pytest

MANIFEST_PATH = "/home/user/manifest.json"
README_PATH = "/home/user/repo/docs/readme.txt"
SETTINGS_PATH = "/home/user/repo/config/settings.conf"
IGNORE_PATH = "/home/user/repo/docs/ignore.log"

def get_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def test_files_converted_to_utf8():
    assert os.path.exists(README_PATH), f"Missing {README_PATH}"
    with open(README_PATH, 'rb') as f:
        readme_content = f.read()

    # Allow with or without trailing newline depending on how echo/student script handled it
    expected_readme_1 = "Documentation for v1.0\nIt “works” well.".encode('utf-8')
    expected_readme_2 = "Documentation for v1.0\nIt “works” well.\n".encode('utf-8')
    assert readme_content in (expected_readme_1, expected_readme_2), "readme.txt was not properly converted to UTF-8"

    assert os.path.exists(SETTINGS_PATH), f"Missing {SETTINGS_PATH}"
    with open(SETTINGS_PATH, 'rb') as f:
        settings_content = f.read()

    expected_settings_1 = "System configuration\nMax connections: 100\nAuthor: René".encode('utf-8')
    expected_settings_2 = "System configuration\nMax connections: 100\nAuthor: René\n".encode('utf-8')
    assert settings_content in (expected_settings_1, expected_settings_2), "settings.conf was not properly converted to UTF-8"

def test_manifest_exists_and_valid():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} is missing"

    with open(MANIFEST_PATH, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest at {MANIFEST_PATH} is not valid JSON")

    assert isinstance(manifest, dict), "Manifest should be a JSON dictionary"

    readme_hash = get_sha256(README_PATH)
    settings_hash = get_sha256(SETTINGS_PATH)

    assert "docs/readme.txt" in manifest, "docs/readme.txt missing from manifest"
    assert manifest["docs/readme.txt"] == readme_hash, "Incorrect SHA-256 hash for docs/readme.txt"

    # settings.conf could be 'config/settings.conf' or 'links/cfg_link/settings.conf'
    found_settings = False
    for k, v in manifest.items():
        if "settings.conf" in k:
            assert v == settings_hash, f"Incorrect SHA-256 hash for {k}"
            found_settings = True

    assert found_settings, "settings.conf missing from manifest"

def test_ignored_files_unchanged():
    assert os.path.exists(IGNORE_PATH), f"Missing {IGNORE_PATH}"
    with open(IGNORE_PATH, 'rb') as f:
        content = f.read()

    # Ignore.log should not have been processed or altered
    assert content in (b"Ignore this file\n", b"Ignore this file"), "ignore.log was modified but should have been ignored"