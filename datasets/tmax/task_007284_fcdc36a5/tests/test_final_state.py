# test_final_state.py
import os
import struct
import pytest

def test_extracted_files():
    """Test that the zip was extracted correctly to /home/user/project_files/."""
    base_dir = "/home/user/project_files"
    assert os.path.isdir(base_dir), f"Directory {base_dir} does not exist."

    expected_files = [
        "compiler_output.log",
        "firmware.elf",
        "main_print.gcode"
    ]
    for f in expected_files:
        filepath = os.path.join(base_dir, f)
        assert os.path.isfile(filepath), f"Expected extracted file {filepath} is missing."

def test_entry_point():
    """Test that the entry point in /home/user/entry_point.txt matches the ELF file."""
    elf_path = "/home/user/project_files/firmware.elf"
    txt_path = "/home/user/entry_point.txt"

    assert os.path.isfile(elf_path), f"Missing {elf_path}"
    assert os.path.isfile(txt_path), f"Missing {txt_path}"

    # Parse ELF entry point manually
    with open(elf_path, "rb") as f:
        e_ident = f.read(16)
        assert e_ident[:4] == b"\x7fELF", f"{elf_path} is not a valid ELF file."
        is_64_bit = e_ident[4] == 2
        endianness = "<" if e_ident[5] == 1 else ">"

        if is_64_bit:
            f.seek(24)
            entry_bytes = f.read(8)
            entry_point = struct.unpack(endianness + "Q", entry_bytes)[0]
        else:
            f.seek(24)
            entry_bytes = f.read(4)
            entry_point = struct.unpack(endianness + "I", entry_bytes)[0]

    with open(txt_path, "r") as f:
        actual_entry_str = f.read().strip()

    try:
        actual_entry = int(actual_entry_str, 16)
    except ValueError:
        pytest.fail(f"Could not parse entry point from {txt_path} as hex: {actual_entry_str}")

    assert entry_point == actual_entry, f"Entry point mismatch. Expected {hex(entry_point)}, got {hex(actual_entry)}"

def test_gcode_chunks():
    """Test that the GCode file was split correctly into chunks."""
    chunks_dir = "/home/user/gcode_chunks"
    assert os.path.isdir(chunks_dir), f"Directory {chunks_dir} does not exist."

    chunk0 = os.path.join(chunks_dir, "chunk_00.gcode")
    chunk1 = os.path.join(chunks_dir, "chunk_01.gcode")
    chunk2 = os.path.join(chunks_dir, "chunk_02.gcode")
    chunk3 = os.path.join(chunks_dir, "chunk_03.gcode")

    assert os.path.isfile(chunk0), f"Missing {chunk0}"
    assert os.path.isfile(chunk1), f"Missing {chunk1}"
    assert os.path.isfile(chunk2), f"Missing {chunk2}"
    assert os.path.isfile(chunk3), f"Missing {chunk3}"

    with open(chunk0, "r") as f:
        lines0 = f.read().splitlines()
    assert len(lines0) == 4, f"{chunk0} should have 4 lines."
    assert "M104 S200" in lines0, f"Missing expected content in {chunk0}"

    with open(chunk1, "r") as f:
        lines1 = f.read().splitlines()
    assert len(lines1) == 3, f"{chunk1} should have 3 lines."
    assert lines1[0] == ";LAYER_CHANGE", f"{chunk1} should start with ;LAYER_CHANGE"
    assert "G1 X20 Y10 F3000" in lines1, f"Missing expected content in {chunk1}"

    with open(chunk2, "r") as f:
        lines2 = f.read().splitlines()
    assert len(lines2) == 3, f"{chunk2} should have 3 lines."
    assert lines2[0] == ";LAYER_CHANGE", f"{chunk2} should start with ;LAYER_CHANGE"

    with open(chunk3, "r") as f:
        lines3 = f.read().splitlines()
    assert len(lines3) == 4, f"{chunk3} should have 4 lines."
    assert lines3[0] == ";LAYER_CHANGE", f"{chunk3} should start with ;LAYER_CHANGE"
    assert "M140 S0" in lines3, f"Missing expected content in {chunk3}"