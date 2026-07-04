# test_final_state.py

import os
import pytest

def test_no_oldconf_files_exist():
    base_dir = "/home/user/configs"
    oldconf_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".oldconf"):
                oldconf_files.append(os.path.join(root, file))
    assert len(oldconf_files) == 0, f"Found .oldconf files that should have been deleted: {oldconf_files}"

def test_app1_settings_newconf():
    file_path = "/home/user/configs/app1/settings.newconf"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The script failed to create it."

    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        pytest.fail(f"File {file_path} is not properly UTF-8 encoded.")

    assert "DEBUG_LEVEL=3" in content, f"DEBUG_LEVEL=3 not found in {file_path}"
    assert "DEBUG_LEVEL=1" not in content, f"DEBUG_LEVEL=1 should have been replaced in {file_path}"
    assert "ENVIRONMENT=production" in content, f"ENVIRONMENT=production not found in {file_path}"
    assert "ENVIRONMENT=staging" not in content, f"ENVIRONMENT=staging should have been replaced in {file_path}"
    assert "Café" in content, f"'Café' not found in {file_path}. Ensure it was decoded from ISO-8859-1 and encoded to UTF-8 correctly."

def test_app2_main_newconf():
    file_path = "/home/user/configs/app2/main.newconf"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The script failed to create it."

    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        pytest.fail(f"File {file_path} is not properly UTF-8 encoded.")

    assert "DEBUG_LEVEL=3" in content, f"DEBUG_LEVEL=3 not found in {file_path}"
    assert "DEBUG_LEVEL=1" not in content, f"DEBUG_LEVEL=1 should have been replaced in {file_path}"
    assert "ENVIRONMENT=production" in content, f"ENVIRONMENT=production not found in {file_path}"
    assert "ENVIRONMENT=staging" not in content, f"ENVIRONMENT=staging should have been replaced in {file_path}"

def test_app2_ignore_me_txt_unchanged():
    file_path = "/home/user/configs/app2/ignore_me.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. It should not have been deleted."

    with open(file_path, "r", encoding="UTF-8") as f:
        content = f.read()

    assert "DEBUG_LEVEL=1" in content, f"File {file_path} was incorrectly modified."
    assert "DEBUG_LEVEL=3" not in content, f"File {file_path} was incorrectly modified."

def test_symlink_loop_exists():
    symlink_path = "/home/user/configs/app1/backup_loop"
    assert os.path.islink(symlink_path), f"Symlink {symlink_path} does not exist. It should not have been removed."
    target = os.readlink(symlink_path)
    assert target == "/home/user/configs", f"Symlink {symlink_path} points to the wrong target."