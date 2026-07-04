# test_final_state.py
import os
import pytest

INDEX_FILE = "/home/user/curated_index.txt"
BASE_DIR = "/home/user/artifacts"

def get_expected_entries():
    """
    Derives the expected output by walking the directory tree,
    avoiding symlinks, and finding .blob files > 100,000 bytes.
    """
    entries = []
    for root, dirs, files in os.walk(BASE_DIR):
        for filename in files:
            if not filename.endswith(".blob"):
                continue

            filepath = os.path.join(root, filename)

            # Skip if it's a symlink
            if os.path.islink(filepath):
                continue

            try:
                size = os.path.getsize(filepath)
            except OSError:
                continue

            if size > 100000:
                with open(filepath, "rb") as f:
                    data = f.read(32)
                hex_str = data.hex()
                entries.append(f"{filepath}: {hex_str}")

    # Sort alphabetically by absolute file path
    entries.sort()
    return entries

def test_curated_index_exists():
    assert os.path.isfile(INDEX_FILE), f"Verification failed: {INDEX_FILE} not found."

def test_curated_index_contents():
    expected_lines = get_expected_entries()

    with open(INDEX_FILE, "r") as f:
        actual_content = f.read()

    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines_stripped = [line.strip() for line in expected_lines]

    assert actual_lines == expected_lines_stripped, (
        f"Verification failed: The contents of {INDEX_FILE} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines_stripped)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )

def test_symlinks_untouched():
    link1 = os.path.join(BASE_DIR, "archive_A", "link_to_B")
    link2 = os.path.join(BASE_DIR, "archive_B", "nested", "link_to_A")

    assert os.path.islink(link1), f"Symlink was modified or removed: {link1}"
    assert os.path.islink(link2), f"Symlink was modified or removed: {link2}"

    assert os.readlink(link1) == os.path.join(BASE_DIR, "archive_B"), f"Symlink target was altered for {link1}"
    assert os.readlink(link2) == os.path.join(BASE_DIR, "archive_A"), f"Symlink target was altered for {link2}"