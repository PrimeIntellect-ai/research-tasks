# test_final_state.py

import os
import json
import pytest

def test_libauth_c_patched():
    filepath = "/home/user/app/src/libauth.c"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read()

    assert "strncpy" in content, "libauth.c was not patched correctly: missing 'strncpy'."
    assert "strcpy(" not in content, "libauth.c was not patched correctly: 'strcpy' is still present."

def test_shared_library_compiled():
    filepath = "/home/user/app/build/libauth.so.1.0.1"
    assert os.path.isfile(filepath), f"Compiled library {filepath} does not exist."

    with open(filepath, "rb") as f:
        magic = f.read(4)

    assert magic == b"\x7fELF", f"File {filepath} is not a valid ELF binary."

def test_shared_library_symlink():
    symlink_path = "/home/user/app/build/libauth.so"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    target = os.readlink(symlink_path)
    # The symlink can be absolute or relative, but it should resolve to the correct file
    resolved_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
    expected_target = "/home/user/app/build/libauth.so.1.0.1"

    assert resolved_target == expected_target, f"Symlink {symlink_path} does not point to {expected_target}."

def test_manifest_updated():
    filepath = "/home/user/app/manifest.json"
    assert os.path.isfile(filepath), f"Manifest file {filepath} does not exist."

    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest file {filepath} is not valid JSON.")

    assert "components" in data, "manifest.json missing 'components' key."
    assert "libauth" in data["components"], "manifest.json missing 'libauth' component."
    assert data["components"]["libauth"].get("version") == "1.0.1", "libauth version in manifest.json was not updated to '1.0.1'."

def test_update_script_exists():
    filepath = "/home/user/app/update_manifest.py"
    assert os.path.isfile(filepath), f"Python script {filepath} does not exist."

def test_e2e_test_results():
    filepath = "/home/user/app/test_results.log"
    assert os.path.isfile(filepath), f"Test results file {filepath} does not exist. Did you run the e2e test script?"

    with open(filepath, "r") as f:
        content = f.read()

    assert content == "E2E SEC TEST: PASS\n", f"Test results file content is incorrect. Got: {repr(content)}"