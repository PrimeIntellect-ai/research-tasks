# test_final_state.py

import os
import re

def test_extract_headers_source():
    src_file = '/home/user/extract_headers.c'
    assert os.path.isfile(src_file), f"C source file {src_file} does not exist."

    with open(src_file, 'r') as f:
        content = f.read()

    # Check for atomic write using rename
    assert re.search(r'\brename\s*\(', content), "The C program does not appear to use rename() for atomic writes."
    assert "inventory.csv.tmp" in content, "The C program does not reference the temporary file inventory.csv.tmp."

def test_extract_headers_executable():
    exe_file = '/home/user/extract_headers'
    assert os.path.isfile(exe_file), f"Compiled executable {exe_file} does not exist."
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

def test_inventory_csv():
    inv_file = '/home/user/inventory.csv'
    assert os.path.isfile(inv_file), f"Inventory file {inv_file} does not exist."

    with open(inv_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "alpha.art,Alpha-Build,1,100",
        "beta.art,Beta-Core,2,250",
        "delta.art,Delta-Engine,3,500",
        "gamma.art,Gamma-Module,1,50"
    }

    actual_lines = set(lines)
    assert actual_lines == expected_lines, f"Contents of {inv_file} do not match expected metadata."

def test_final_inventory_csv():
    final_inv_file = '/home/user/final_inventory.csv'
    assert os.path.isfile(final_inv_file), f"Final inventory file {final_inv_file} does not exist."

    with open(final_inv_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "alpha.art,Alpha-Build,1,100",
        "gamma.art,Gamma-Module,1,50"
    }

    actual_lines = set(lines)
    assert actual_lines == expected_lines, f"Contents of {final_inv_file} do not match expected filtered metadata."

def test_backup_status():
    status_file = '/home/user/backup_status.txt'
    assert os.path.isfile(status_file), f"Backup status file {status_file} does not exist."

    with open(status_file, 'r') as f:
        content = f.read().strip()

    assert content == "CORRUPT", f"Expected backup status to be 'CORRUPT', but got '{content}'."