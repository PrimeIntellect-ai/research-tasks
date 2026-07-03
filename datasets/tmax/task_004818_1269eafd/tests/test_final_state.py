# test_final_state.py

import os
import re
import pytest

SCRIPT_PATH = "/home/user/curate_repo.sh"
CONFIG_PATH = "/home/user/repo_config.ini"
META1_PATH = "/home/user/artifact_repo/groupA/artifact1.meta"
META2_PATH = "/home/user/artifact_repo/groupB/artifact2.meta"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_logic():
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        script_content = f.read()

    # Check for dynamic parsing (should not hardcode the old prefix)
    assert "C:\\OldSystem\\Binaries\\" not in script_content, \
        "Script should not hardcode the OldPrefix 'C:\\OldSystem\\Binaries\\'."
    assert "/opt/new_system/artifacts/" not in script_content, \
        "Script should not hardcode the NewPrefix '/opt/new_system/artifacts/'."

    # Check for atomic writes
    assert ".tmp" in script_content, "Script must use a .tmp file for atomic writes."
    assert "mv " in script_content, "Script must use 'mv' to atomically replace the original file."

def test_meta_files_encoded_utf8():
    for meta_path in [META1_PATH, META2_PATH]:
        assert os.path.exists(meta_path), f"File {meta_path} is missing."

        # If it was UTF-16LE, reading as UTF-8 would likely fail or have null bytes
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                content = f.read()
                assert "\x00" not in content, f"File {meta_path} still appears to be UTF-16 encoded (contains null bytes)."
        except UnicodeDecodeError:
            pytest.fail(f"File {meta_path} could not be decoded as UTF-8.")

def test_meta_files_content_updated():
    # Read config to get expected replacement
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config_content = f.read()

    old_prefix = re.search(r"OldPrefix=(.*)", config_content).group(1).strip()
    new_prefix = re.search(r"NewPrefix=(.*)", config_content).group(1).strip()

    with open(META1_PATH, "r", encoding="utf-8") as f:
        content1 = f.read()

    assert old_prefix not in content1, f"Old prefix {old_prefix} still found in {META1_PATH}."
    assert f"Path={new_prefix}groupA/artifact1.bin" in content1, f"New path not correctly set in {META1_PATH}."

    with open(META2_PATH, "r", encoding="utf-8") as f:
        content2 = f.read()

    assert old_prefix not in content2, f"Old prefix {old_prefix} still found in {META2_PATH}."
    assert f"Path={new_prefix}groupB/artifact2.bin" in content2, f"New path not correctly set in {META2_PATH}."