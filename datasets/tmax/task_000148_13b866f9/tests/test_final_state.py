# test_final_state.py

import os
import json
import pytest

def test_script_exists_and_uses_flock():
    script_path = "/home/user/index_docs.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "fcntl" in content and "flock" in content, "The script must use fcntl.flock for exclusive file locking."

def test_zip_slip_not_extracted():
    hacked_file = "/home/user/hacked.txt"
    assert not os.path.exists(hacked_file), "Zip slip vulnerability triggered! Malicious file was extracted."

def test_doc_index_jsonl_content():
    index_path = "/home/user/doc_index.jsonl"
    assert os.path.isfile(index_path), f"Output file {index_path} does not exist."

    parsed_lines = []
    with open(index_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    parsed_lines.append(json.loads(line))
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON line in {index_path}: {line}")

    assert len(parsed_lines) == 2, f"Expected 2 lines in {index_path}, found {len(parsed_lines)}"

    # Create a dictionary mapping archive name to its data for easy checking
    results = {item.get("archive"): item for item in parsed_lines}

    assert "release_v1.zip" in results, "Missing entry for release_v1.zip"
    assert "release_v2.zip" in results, "Missing entry for release_v2.zip"

    # Check release_v1.zip
    v1_data = results["release_v1.zip"]
    assert "elf_entry_points" in v1_data, "Missing elf_entry_points in release_v1.zip entry"
    assert "firmware_main.elf" in v1_data["elf_entry_points"], "Missing firmware_main.elf entry point"
    v1_elf = v1_data["elf_entry_points"]["firmware_main.elf"]
    assert int(v1_elf, 16) == 0x400080, f"Incorrect entry point for firmware_main.elf: {v1_elf}"

    assert "gcode_machines" in v1_data, "Missing gcode_machines in release_v1.zip entry"
    assert "case_part.gcode" in v1_data["gcode_machines"], "Missing case_part.gcode machine name"
    assert v1_data["gcode_machines"]["case_part.gcode"] == "Prusa i3 MK3S", "Incorrect machine name for case_part.gcode"

    # Check release_v2.zip
    v2_data = results["release_v2.zip"]
    assert "elf_entry_points" in v2_data, "Missing elf_entry_points in release_v2.zip entry"
    assert "bootloader.elf" in v2_data["elf_entry_points"], "Missing bootloader.elf entry point"
    v2_elf = v2_data["elf_entry_points"]["bootloader.elf"]
    assert int(v2_elf, 16) == 0x08000000, f"Incorrect entry point for bootloader.elf: {v2_elf}"

    assert "gcode_machines" in v2_data, "Missing gcode_machines in release_v2.zip entry"
    assert "jig.gcode" in v2_data["gcode_machines"], "Missing jig.gcode machine name"
    assert v2_data["gcode_machines"]["jig.gcode"] == "Ender 3 Pro", "Incorrect machine name for jig.gcode"