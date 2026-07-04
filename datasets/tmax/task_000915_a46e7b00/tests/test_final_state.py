# test_final_state.py

import os
import stat

def test_script_exists_and_executable():
    script_path = "/home/user/track_configs.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), \
        f"The script {script_path} is not executable."

def test_script_uses_flock():
    script_path = "/home/user/track_configs.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "flock" in content, f"The script {script_path} does not use 'flock' as required."

def test_inventory_file_contents():
    inventory_path = "/home/user/config_inventory.txt"
    assert os.path.isfile(inventory_path), f"The inventory file {inventory_path} does not exist. Did you run the script?"

    with open(inventory_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "app_new.json:1.2.3",
        "cache_new.xml:2.0.0-rc1",
        "db_new.csv:9.5.1"
    }

    unexpected_lines = {
        "app_old.json:0.9.0",
        "web_old.xml:1.0.0"
    }

    actual_lines_set = set(lines)

    missing = expected_lines - actual_lines_set
    assert not missing, f"The inventory file is missing expected entries: {missing}"

    extra = actual_lines_set - expected_lines
    assert not extra, f"The inventory file contains unexpected entries (perhaps old files or incorrect parsing): {extra}"