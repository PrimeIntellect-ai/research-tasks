# test_final_state.py
import os
import hashlib
import re

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def test_script_exists_and_uses_mv():
    script_path = "/home/user/organize.sh"
    assert os.path.isfile(script_path), f"Script {script_path} not found."
    with open(script_path, 'r') as f:
        content = f.read()
    # Check for mv command usage (simplistic check for atomic write requirement)
    assert re.search(r'\bmv\b', content), "Script does not appear to use 'mv' for atomic writes."

def test_organized_files_and_inventory():
    project_dump = "/home/user/project_dump"
    elf64_dir = "/home/user/organized/elf64"
    wal_dir = "/home/user/organized/wal"
    inventory_path = "/home/user/inventory.txt"

    assert os.path.isfile(inventory_path), f"Inventory file {inventory_path} not found."

    expected_elf64 = []
    expected_wal = []

    # Traverse project_dump to find expected files
    for root, dirs, files in os.walk(project_dump):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'rb') as f:
                header = f.read(7)

            if header.startswith(b'\x7f\x45\x4c\x46\x02'):
                expected_elf64.append(filepath)
            elif header.startswith(b'WAL_v3\x00'):
                expected_wal.append(filepath)

    assert len(expected_elf64) > 0, "No ELF64 files found in source."
    assert len(expected_wal) > 0, "No WAL files found in source."

    expected_mappings = {}

    for filepath in expected_elf64:
        h = get_sha256(filepath)
        dest = os.path.join(elf64_dir, h)
        expected_mappings[filepath] = dest
        assert os.path.isfile(dest), f"Expected ELF64 file {dest} not found."
        assert get_sha256(dest) == h, f"Content mismatch for {dest}."

    for filepath in expected_wal:
        h = get_sha256(filepath)
        dest = os.path.join(wal_dir, h)
        expected_mappings[filepath] = dest
        assert os.path.isfile(dest), f"Expected WAL file {dest} not found."
        assert get_sha256(dest) == h, f"Content mismatch for {dest}."

    # Check inventory
    with open(inventory_path, 'r') as f:
        inventory_lines = [line.strip() for line in f if line.strip()]

    assert len(inventory_lines) == len(expected_mappings), "Inventory line count mismatch."

    for line in inventory_lines:
        parts = line.split(" -> ")
        assert len(parts) == 2, f"Invalid inventory line format: {line}"
        src, dest = parts
        assert src in expected_mappings, f"Unexpected source file in inventory: {src}"
        assert expected_mappings[src] == dest, f"Incorrect destination in inventory for {src}: expected {expected_mappings[src]}, got {dest}"

    # Check for unexpected files in target dirs
    elf64_files = os.listdir(elf64_dir)
    assert len(elf64_files) == len(expected_elf64), "Unexpected files found in elf64 directory."

    wal_files = os.listdir(wal_dir)
    assert len(wal_files) == len(expected_wal), "Unexpected files found in wal directory."