# test_final_state.py

import os
import json
import pytest

INVENTORY_PATH = "/home/user/organized_elfs/inventory.json"
MESSY_DIR = "/home/user/messy_project"

def test_inventory_exists_and_valid():
    assert os.path.isfile(INVENTORY_PATH), f"{INVENTORY_PATH} does not exist."
    with open(INVENTORY_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{INVENTORY_PATH} is not valid JSON.")

    assert isinstance(data, list), "Inventory JSON should be a list of objects."

    expected_files = {"app_64", "app_32", "libtest.so"}
    found_files = set()

    for entry in data:
        assert "original_path" in entry, "Missing original_path in entry"
        assert "linked_path" in entry, "Missing linked_path in entry"
        assert "machine" in entry, "Missing machine in entry"
        assert "type" in entry, "Missing type in entry"

        orig_path = entry["original_path"]
        linked_path = entry["linked_path"]

        assert os.path.isfile(orig_path), f"Original path {orig_path} does not exist."
        assert os.path.isfile(linked_path), f"Linked path {linked_path} does not exist."

        orig_stat = os.stat(orig_path)
        link_stat = os.stat(linked_path)

        assert orig_stat.st_ino == link_stat.st_ino, f"File {linked_path} is not a hardlink to {orig_path}."

        filename = os.path.basename(orig_path)
        found_files.add(filename)

        # Verify cleaning logic
        machine_clean = entry["machine"].replace(" ", "_").replace("(", "").replace(")", "")
        type_clean = entry["type"].replace(" ", "_").replace("(", "").replace(")", "")

        expected_linked_path = os.path.join("/home/user/organized_elfs", machine_clean, type_clean, filename)
        assert linked_path == expected_linked_path, f"Linked path {linked_path} does not match expected {expected_linked_path}"

    assert expected_files.issubset(found_files), f"Missing ELF files in inventory. Expected {expected_files}, found {found_files}"

    # Check that non-ELF files are not included
    assert "main.c" not in found_files, "main.c should not be in the inventory"
    assert "build.log" not in found_files, "build.log should not be in the inventory"

def test_atomic_write_logic_in_scripts():
    # Search for scripts in /home/user/ that mention inventory.json
    found_atomic = False
    script_found = False
    for root, dirs, files in os.walk("/home/user"):
        if "organized_elfs" in root or "messy_project" in root:
            continue
        for file in files:
            if file.endswith((".py", ".sh", ".rb")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        if "inventory.json" in content:
                            script_found = True
                            if "replace" in content or "rename" in content or "mv " in content:
                                found_atomic = True
                except Exception:
                    pass

    if script_found:
        assert found_atomic, "Script found but does not appear to use atomic write (rename/replace/mv)."
    # If no script is found, we can't strictly fail because they might have run it interactively, 
    # but the prompt implies a script should exist. We'll pass if script is missing to avoid false negatives 
    # if they deleted it, but ideally they left it.