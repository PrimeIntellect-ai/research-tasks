# test_final_state.py

import os
import json
import subprocess
import pytest

def test_target_files_txt():
    """Check that target_files.txt contains the correct filenames extracted from the log."""
    target_files_path = "/home/user/target_files.txt"
    assert os.path.isfile(target_files_path), f"File {target_files_path} does not exist."

    with open(target_files_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {target_files_path}, found {len(lines)}."
    assert lines[0] == "sys_true", f"Expected first line to be 'sys_true', got '{lines[0]}'."
    assert lines[1] == "sys_false", f"Expected second line to be 'sys_false', got '{lines[1]}'."

def test_rust_project_exists():
    """Check that the Rust Cargo project was created and uses goblin."""
    cargo_toml_path = "/home/user/elf_inspector/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), f"Rust project Cargo.toml not found at {cargo_toml_path}."

    with open(cargo_toml_path, "r") as f:
        content = f.read()

    assert "goblin" in content, "The 'goblin' crate is missing from Cargo.toml dependencies."

def get_elf_entry(filepath):
    """Helper to extract the entry point of an ELF file using readelf."""
    try:
        entry_out = subprocess.check_output(f"readelf -h {filepath} | grep 'Entry point address:'", shell=True).decode()
        entry_hex = entry_out.split(":", 1)[1].strip()
        return int(entry_hex, 16)
    except Exception as e:
        pytest.fail(f"Failed to read ELF entry point for {filepath}: {e}")

def test_final_report_jsonl():
    """Check that the final_report.jsonl contains the correct parsed ELF metadata."""
    report_path = "/home/user/final_report.jsonl"
    assert os.path.isfile(report_path), f"Final report file {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 JSON lines in {report_path}, found {len(lines)}."

    try:
        data1 = json.loads(lines[0])
        data2 = json.loads(lines[1])
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON lines from report: {e}")

    expected_true_entry = get_elf_entry("/home/user/artifacts/sys_true")
    expected_false_entry = get_elf_entry("/home/user/artifacts/sys_false")

    # Check first object
    assert "file" in data1, "Missing 'file' key in first JSON object."
    assert "machine" in data1, "Missing 'machine' key in first JSON object."
    assert "entry" in data1, "Missing 'entry' key in first JSON object."

    assert data1["file"] == "sys_true", f"First file must be 'sys_true', got '{data1['file']}'."
    assert isinstance(data1["machine"], int), "The 'machine' value must be an integer."
    assert data1["entry"] == expected_true_entry, f"sys_true entry point mismatch. Expected {expected_true_entry}, got {data1['entry']}."

    # Check second object
    assert "file" in data2, "Missing 'file' key in second JSON object."
    assert "machine" in data2, "Missing 'machine' key in second JSON object."
    assert "entry" in data2, "Missing 'entry' key in second JSON object."

    assert data2["file"] == "sys_false", f"Second file must be 'sys_false', got '{data2['file']}'."
    assert isinstance(data2["machine"], int), "The 'machine' value must be an integer."
    assert data2["entry"] == expected_false_entry, f"sys_false entry point mismatch. Expected {expected_false_entry}, got {data2['entry']}."