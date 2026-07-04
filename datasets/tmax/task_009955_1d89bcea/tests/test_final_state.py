# test_final_state.py

import os
import pytest

def decode_zxt(path):
    """Decodes a .zxt file according to the custom RLE and UTF-16LE format."""
    with open(path, 'rb') as f:
        data = f.read()

    result = []
    for i in range(0, len(data), 3):
        chunk = data[i:i+3]
        if len(chunk) < 3:
            break
        count = chunk[0]
        char = chunk[1:3].decode('utf-16le')
        result.append(char * count)
    return "".join(result)

def get_expected_summary():
    """Dynamically traverses the directory, avoids loops, and generates the expected summary."""
    base_dir = "/home/user/storage_data"
    visited_dirs = set()
    unique_files = set()

    def traverse(current_path):
        real_current = os.path.realpath(current_path)
        if real_current in visited_dirs:
            return
        visited_dirs.add(real_current)

        try:
            entries = os.listdir(current_path)
        except OSError:
            return

        for entry in entries:
            full_path = os.path.join(current_path, entry)
            if os.path.isdir(full_path):
                traverse(full_path)
            else:
                if full_path.endswith('.zxt'):
                    real_file = os.path.realpath(full_path)
                    unique_files.add(real_file)

    traverse(base_dir)

    lines = []
    for f in sorted(list(unique_files)):
        decoded = decode_zxt(f)
        lines.append(f"{f}: {decoded}")

    if not lines:
        return ""
    return "\n".join(lines) + "\n"

def test_decompress_files_exist():
    """Verify that the C source and compiled executable exist."""
    c_file = "/home/user/decompress.c"
    exe_file = "/home/user/decompress"

    assert os.path.isfile(c_file), f"C source file missing at {c_file}"
    assert os.path.isfile(exe_file), f"Compiled executable missing at {exe_file}"
    assert os.access(exe_file, os.X_OK), f"File at {exe_file} is not executable"

def test_summary_log_correct():
    """Verify that the summary.log contains the exactly correct, deduplicated, sorted output."""
    summary_file = "/home/user/summary.log"
    assert os.path.isfile(summary_file), f"Summary log missing at {summary_file}"

    with open(summary_file, "r", encoding="utf-8") as f:
        actual_content = f.read()

    expected_content = get_expected_summary()

    # Compare line by line for better error messages
    actual_lines = actual_content.strip().split('\n') if actual_content.strip() else []
    expected_lines = expected_content.strip().split('\n') if expected_content.strip() else []

    assert actual_lines == expected_lines, (
        "The contents of summary.log do not match the expected output. "
        "Ensure you followed symlinks, avoided loops, processed each physical file exactly once, "
        "decoded correctly, and sorted by absolute resolved path."
    )