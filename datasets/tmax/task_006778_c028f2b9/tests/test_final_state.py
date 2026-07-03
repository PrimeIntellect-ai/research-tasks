# test_final_state.py

import os
import struct

def rle_decompress(data):
    decompressed = bytearray()
    for i in range(0, len(data), 2):
        if i + 1 >= len(data):
            break
        count, char = struct.unpack('BB', data[i:i+2])
        decompressed.extend(bytes([char]) * count)
    return decompressed.decode('utf-8')

def test_error_summary_log_exists_and_correct():
    """Test that error_summary.log is correctly generated based on the .clog files."""
    base_dir = "/home/user/project_logs"
    summary_path = "/home/user/error_summary.log"

    assert os.path.exists(summary_path), f"File {summary_path} does not exist."
    assert os.path.isfile(summary_path), f"Path {summary_path} is not a file."

    errors = []

    # Traverse and decompress to find expected errors
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".clog"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)

                with open(full_path, "rb") as f:
                    data = f.read()

                text = rle_decompress(data)

                records = []
                current_record = []
                for line in text.splitlines(keepends=True):
                    if line.startswith('['):
                        if current_record:
                            records.append("".join(current_record))
                        current_record = [line]
                    else:
                        current_record.append(line)
                if current_record:
                    records.append("".join(current_record))

                for record in records:
                    if "] ERROR:" in record:
                        errors.append((rel_path, record))

    # Sort alphabetically by relative path
    errors.sort(key=lambda x: x[0])

    expected_output = ""
    for rel_path, record in errors:
        expected_output += "---\n"
        expected_output += f"File: {rel_path}\n"
        expected_output += record

    with open(summary_path, "r", encoding="utf-8") as f:
        actual_output = f.read()

    assert actual_output == expected_output, (
        f"Contents of {summary_path} do not match the expected output.\n"
        f"Expected:\n{expected_output}\n\nActual:\n{actual_output}"
    )