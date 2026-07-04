# test_final_state.py

import os
import pytest

BASE_DIR = '/home/user/project_dump'
REPORT_FILE = '/home/user/report.txt'

def test_report_file():
    assert os.path.exists(REPORT_FILE), f"Report file {REPORT_FILE} is missing."
    with open(REPORT_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "Report file must contain at least two lines."
    assert lines[0] == '5', f"Expected 5 total .txt files processed, got {lines[0]}"
    assert lines[1] == '2', f"Expected 2 hard links created, got {lines[1]}"

def test_files_are_utf8():
    expected_contents = {
        "module_a/desc.txt": "Résumé of the café project.",
        "module_b/notes.txt": "こんにちは世界",
        "module_b/desc_backup.txt": "Résumé of the café project.",
        "docs/ReadMe.txt": "How to use this system.",
        "docs/intro.txt": "Résumé of the café project.",
    }

    for rel_path, expected_text in expected_contents.items():
        full_path = os.path.join(BASE_DIR, rel_path)
        assert os.path.exists(full_path), f"File {full_path} is missing."
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            assert content == expected_text, f"Content mismatch in {full_path}. Expected '{expected_text}', got '{content}'"
        except UnicodeDecodeError:
            pytest.fail(f"File {full_path} is not valid UTF-8.")

def test_hard_link_deduplication():
    file1 = os.path.join(BASE_DIR, "module_a/desc.txt")
    file2 = os.path.join(BASE_DIR, "module_b/desc_backup.txt")
    file3 = os.path.join(BASE_DIR, "docs/intro.txt")

    assert os.path.exists(file1), f"Missing {file1}"
    assert os.path.exists(file2), f"Missing {file2}"
    assert os.path.exists(file3), f"Missing {file3}"

    stat1 = os.stat(file1)
    stat2 = os.stat(file2)
    stat3 = os.stat(file3)

    assert stat1.st_ino == stat2.st_ino == stat3.st_ino, "Files with identical content were not hard-linked to the same inode."

def test_symlink_created():
    symlink_path = os.path.join(BASE_DIR, "docs/README.md")
    target_path = os.path.join(BASE_DIR, "docs/ReadMe.txt")

    assert os.path.exists(symlink_path), f"Symlink {symlink_path} is missing."
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    # Check that it points to ReadMe.txt
    target = os.readlink(symlink_path)
    # The symlink could be absolute or relative. If relative, it should be 'ReadMe.txt' or './ReadMe.txt'
    # Let's resolve both to absolute paths to be sure.
    abs_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
    assert abs_target == os.path.abspath(target_path), f"Symlink {symlink_path} points to {target}, expected {target_path}"