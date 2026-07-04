# test_final_state.py

import os
import pytest

def test_script_exists():
    script_path = "/home/user/scan_dataset.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_inventory_exists_and_correct():
    inventory_path = "/home/user/dataset_inventory.txt"
    assert os.path.isfile(inventory_path), f"The output file {inventory_path} does not exist."

    expected_lines = [
        "/home/user/dataset/binary_tool: ELF",
        "/home/user/dataset/exp_a/broken.gcode: UNKNOWN",
        "/home/user/dataset/exp_a/cache.wal: WAL",
        "/home/user/dataset/exp_a/helper_bin: ELF",
        "/home/user/dataset/exp_b/db.wal: WAL",
        "/home/user/dataset/exp_b/empty.dat: UNKNOWN",
        "/home/user/dataset/exp_b/nested/print_2.gcode: GCODE",
        "/home/user/dataset/notes.txt: UNKNOWN",
        "/home/user/dataset/print_1.gcode: GCODE"
    ]

    with open(inventory_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {inventory_path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )