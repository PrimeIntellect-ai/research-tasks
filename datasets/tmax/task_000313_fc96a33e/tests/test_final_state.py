# test_final_state.py

import os
import hashlib
import pytest

def get_expected_manifest():
    files_to_hash = [
        "/home/user/storage/docs/legacy_notes.txt",
        "/home/user/storage/docs/report.txt",
        "/home/user/storage/images/photo.png"
    ]

    manifest_lines = []
    for filepath in files_to_hash:
        assert os.path.isfile(filepath), f"Expected file {filepath} is missing from the system."
        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        manifest_lines.append(f"{file_hash} *{filepath}")

    # Sort alphabetically by path (which is at the end of the line, but sorting the whole line works 
    # since the hash length is constant and the paths are the primary difference if we sort by path. 
    # Wait, the prompt says "sorted alphabetically by the absolute file path". Let's sort by path explicitly.)
    manifest_lines.sort(key=lambda x: x.split(" *")[1])

    return "\n".join(manifest_lines) + "\n"

def test_manifest_exists():
    manifest_path = "/home/user/backed_up_manifest.txt"
    assert os.path.isfile(manifest_path), f"Output manifest file {manifest_path} was not created."

def test_manifest_encoding_and_content():
    manifest_path = "/home/user/backed_up_manifest.txt"

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            actual_content = f.read()
    except UnicodeDecodeError:
        pytest.fail(f"Manifest file {manifest_path} is not encoded in valid UTF-8.")

    expected_content = get_expected_manifest()

    actual_lines = [line for line in actual_content.splitlines() if line.strip()]
    expected_lines = [line for line in expected_content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in manifest, but found {len(actual_lines)}."

    for i, (actual_line, expected_line) in enumerate(zip(actual_lines, expected_lines)):
        assert actual_line == expected_line, f"Line {i+1} mismatch.\nExpected: {expected_line}\nActual:   {actual_line}"