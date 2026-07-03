# test_final_state.py

import os
import json
import subprocess
import struct
import pytest

COMMITTED_FILES_TXT = "/home/user/data/committed_files.txt"
SUMMARY_JSON = "/home/user/data/summary.json"
WAL_FILE = "/home/user/data/sync.wal"
GCODE_SYMLINK = "/home/user/latest_configs/latest_cnc.gcode"
ELF_SYMLINK = "/home/user/latest_configs/latest_firmware.elf"

def get_expected_committed_files():
    """Derive expected committed files from the WAL file."""
    committed = []
    if os.path.exists(WAL_FILE):
        with open(WAL_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3 and parts[0] == "COMMIT":
                    committed.append(parts[2])
    return committed

def test_committed_files_list():
    assert os.path.exists(COMMITTED_FILES_TXT), f"Missing {COMMITTED_FILES_TXT}"
    with open(COMMITTED_FILES_TXT, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = get_expected_committed_files()
    assert len(expected) > 0, "Expected to find COMMIT lines in WAL file."
    assert set(lines) == set(expected), f"Committed files list does not match WAL COMMIT entries. Expected {expected}, got {lines}"

def test_gcode_encoding_is_utf8():
    expected = get_expected_committed_files()
    gcode_files = [f for f in expected if f.endswith(".gcode")]
    for gcode_file in gcode_files:
        assert os.path.exists(gcode_file), f"GCode file missing: {gcode_file}"
        try:
            with open(gcode_file, "r", encoding="utf-8") as f:
                f.read()
        except UnicodeDecodeError:
            pytest.fail(f"GCode file {gcode_file} is not valid UTF-8.")

def test_go_code_exists():
    assert os.path.exists("/home/user/parser/main.go"), "Go source file missing at /home/user/parser/main.go"
    assert os.path.exists("/home/user/parser/go.mod"), "Go module file missing at /home/user/parser/go.mod"

def get_elf_info(elf_path):
    """Extract entry point and machine type using readelf to mimic Go's debug/elf."""
    out = subprocess.check_output(["readelf", "-h", elf_path], text=True)
    entry_point = None
    machine = None
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("Entry point address:"):
            val = line.split(":", 1)[1].strip()
            entry_point = int(val, 16)
        elif line.startswith("Machine:"):
            val = line.split(":", 1)[1].strip()
            if "X86-64" in val or "x86-64" in val or "Advanced Micro Devices X86-64" in val:
                machine = "EM_X86_64"
            elif "AArch64" in val:
                machine = "EM_AARCH64"
            elif "80386" in val:
                machine = "EM_386"
            elif "ARM" in val:
                machine = "EM_ARM"
            else:
                machine = val # Fallback, might fail comparison but better than nothing
    return entry_point, machine

def get_max_z(gcode_path):
    """Calculate the max Z from G0/G1 commands."""
    max_z = None
    with open(gcode_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.split(";")[0].strip()
            parts = line.split()
            if not parts:
                continue
            if parts[0] in ("G0", "G1"):
                for p in parts[1:]:
                    if p.startswith("Z"):
                        try:
                            z_val = float(p[1:])
                            if max_z is None or z_val > max_z:
                                max_z = z_val
                        except ValueError:
                            pass
    return max_z

def test_summary_json():
    assert os.path.exists(SUMMARY_JSON), f"Missing {SUMMARY_JSON}"
    with open(SUMMARY_JSON, "r", encoding="utf-8") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{SUMMARY_JSON} is not valid JSON.")

    assert isinstance(summary, list), "Summary JSON must be an array of objects."

    expected_files = get_expected_committed_files()

    summary_by_file = {item.get("file"): item for item in summary}

    for fpath in expected_files:
        assert fpath in summary_by_file, f"File {fpath} missing from summary.json"
        item = summary_by_file[fpath]

        if fpath.endswith(".gcode"):
            assert item.get("type") == "gcode", f"Expected type 'gcode' for {fpath}"
            expected_z = get_max_z(fpath)
            assert "max_z" in item, f"Missing 'max_z' for {fpath}"
            # Float comparison
            assert abs(item["max_z"] - expected_z) < 1e-6, f"Incorrect max_z for {fpath}. Expected {expected_z}, got {item['max_z']}"

        elif fpath.endswith(".elf"):
            assert item.get("type") == "elf", f"Expected type 'elf' for {fpath}"
            expected_entry, expected_machine = get_elf_info(fpath)
            assert "entry_point" in item, f"Missing 'entry_point' for {fpath}"
            assert item["entry_point"] == expected_entry, f"Incorrect entry_point for {fpath}. Expected {expected_entry}, got {item['entry_point']}"
            assert "machine" in item, f"Missing 'machine' for {fpath}"
            assert item["machine"] == expected_machine, f"Incorrect machine for {fpath}. Expected {expected_machine}, got {item['machine']}"

def test_symlinks_created():
    expected_files = get_expected_committed_files()
    gcode_files = [f for f in expected_files if f.endswith(".gcode")]
    elf_files = [f for f in expected_files if f.endswith(".elf")]

    if gcode_files:
        assert os.path.islink(GCODE_SYMLINK), f"Missing or invalid symlink at {GCODE_SYMLINK}"
        target = os.readlink(GCODE_SYMLINK)
        # Handle relative or absolute symlinks
        abs_target = os.path.abspath(os.path.join(os.path.dirname(GCODE_SYMLINK), target))
        assert abs_target == gcode_files[0], f"Symlink {GCODE_SYMLINK} points to {abs_target}, expected {gcode_files[0]}"

    if elf_files:
        assert os.path.islink(ELF_SYMLINK), f"Missing or invalid symlink at {ELF_SYMLINK}"
        target = os.readlink(ELF_SYMLINK)
        abs_target = os.path.abspath(os.path.join(os.path.dirname(ELF_SYMLINK), target))
        assert abs_target == elf_files[0], f"Symlink {ELF_SYMLINK} points to {abs_target}, expected {elf_files[0]}"