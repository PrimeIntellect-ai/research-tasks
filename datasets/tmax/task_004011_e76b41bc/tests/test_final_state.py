# test_final_state.py
import os
import json
import hashlib
import pytest

BUILD_SCRIPTS_DIR = "/home/user/build_scripts"
MANIFEST_PATH = "/home/user/build_scripts/manifest.json"
CHECKSUM_SCRIPT_PATH = "/home/user/ci_checksum.py"
EXPECTED_FILES = ["android_build.py", "ios_build.py", "orchestrator.py"]

def test_patch_applied():
    """Verify that the patch was applied correctly to resolve circular imports."""
    android_build_path = os.path.join(BUILD_SCRIPTS_DIR, "android_build.py")
    ios_build_path = os.path.join(BUILD_SCRIPTS_DIR, "ios_build.py")

    assert os.path.isfile(android_build_path), f"Missing {android_build_path}"
    assert os.path.isfile(ios_build_path), f"Missing {ios_build_path}"

    with open(android_build_path, "r") as f:
        android_content = f.read()
        assert "import ios_build" not in android_content, "Patch was not applied to android_build.py (circular import still present)."

    with open(ios_build_path, "r") as f:
        ios_content = f.read()
        assert "import android_build\n" not in ios_content, "Patch was not applied to ios_build.py (old import still present)."
        assert "from android_build import get_shared_config" in ios_content, "Patch was not applied to ios_build.py (new import missing)."

def test_ci_checksum_script_exists():
    """Verify that the checksum script was created."""
    assert os.path.isfile(CHECKSUM_SCRIPT_PATH), f"Checksum script {CHECKSUM_SCRIPT_PATH} is missing."

def test_manifest_exists_and_correct():
    """Verify that manifest.json exists, is valid JSON, and contains the correct checksums."""
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} is missing. Did you run your script?"

    try:
        with open(MANIFEST_PATH, "r") as f:
            actual_manifest = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Manifest file {MANIFEST_PATH} is not valid JSON.")

    assert isinstance(actual_manifest, dict), "Manifest JSON must be a dictionary."

    expected_manifest = {}
    for fname in EXPECTED_FILES:
        path = os.path.join(BUILD_SCRIPTS_DIR, fname)
        assert os.path.isfile(path), f"Expected script {path} is missing."
        with open(path, "rb") as f:
            expected_manifest[fname] = hashlib.sha256(f.read()).hexdigest()

    # Also include any other .py files that might be in the directory, as per instructions "all .py files"
    for fname in os.listdir(BUILD_SCRIPTS_DIR):
        if fname.endswith(".py"):
            path = os.path.join(BUILD_SCRIPTS_DIR, fname)
            with open(path, "rb") as f:
                expected_manifest[fname] = hashlib.sha256(f.read()).hexdigest()

    assert actual_manifest == expected_manifest, "Manifest JSON contents do not match the expected SHA256 checksums of the .py files."