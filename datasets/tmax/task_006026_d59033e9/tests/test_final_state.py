# test_final_state.py
import os
import stat

def test_quarantine_directory():
    quarantine_dir = "/home/user/quarantine"
    assert os.path.isdir(quarantine_dir), f"Directory {quarantine_dir} does not exist."

    expected_files = {"corrupt1.tar.gz", "corrupt2.tar.gz", "corrupt3.zip"}
    actual_files = set(os.listdir(quarantine_dir))

    assert expected_files.issubset(actual_files), f"Quarantine directory is missing files. Expected {expected_files}, found {actual_files}"
    assert actual_files == expected_files, f"Quarantine directory contains unexpected files. Expected {expected_files}, found {actual_files}"

def test_extracted_directory():
    extracted_dir = "/home/user/extracted"
    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist."

    expected_files = [
        "docset1/old.md",
        "docset1/new1.md",
        "docset2/new2.md",
        "docset3/old2.md",
        "docset3/new3.md"
    ]

    for rel_path in expected_files:
        full_path = os.path.join(extracted_dir, rel_path)
        assert os.path.isfile(full_path), f"Extracted file {full_path} is missing."

def test_hardlinks():
    hardlinks_dir = "/home/user/recent_docs/hardlinks"
    assert os.path.isdir(hardlinks_dir), f"Directory {hardlinks_dir} does not exist."

    expected_links = {
        "new1.md": "/home/user/extracted/docset1/new1.md",
        "new2.md": "/home/user/extracted/docset2/new2.md",
        "new3.md": "/home/user/extracted/docset3/new3.md"
    }

    actual_files = set(os.listdir(hardlinks_dir))
    assert actual_files == set(expected_links.keys()), f"Hardlinks directory contains incorrect files. Expected {set(expected_links.keys())}, found {actual_files}"

    for filename, target_path in expected_links.items():
        link_path = os.path.join(hardlinks_dir, filename)
        assert os.path.isfile(link_path), f"Hard link {link_path} is missing."

        # Check if they are actually hard links (same inode)
        link_stat = os.stat(link_path)
        target_stat = os.stat(target_path)
        assert link_stat.st_ino == target_stat.st_ino, f"File {link_path} is not a hardlink to {target_path}."

def test_symlinks():
    symlinks_dir = "/home/user/recent_docs/symlinks"
    assert os.path.isdir(symlinks_dir), f"Directory {symlinks_dir} does not exist."

    expected_links = {
        "new1.md": "/home/user/extracted/docset1/new1.md",
        "new2.md": "/home/user/extracted/docset2/new2.md",
        "new3.md": "/home/user/extracted/docset3/new3.md"
    }

    actual_files = set(os.listdir(symlinks_dir))
    assert actual_files == set(expected_links.keys()), f"Symlinks directory contains incorrect files. Expected {set(expected_links.keys())}, found {actual_files}"

    for filename, target_path in expected_links.items():
        link_path = os.path.join(symlinks_dir, filename)
        assert os.path.islink(link_path), f"File {link_path} is not a symlink."

        # Check if symlink points to the correct absolute path
        actual_target = os.readlink(link_path)
        assert actual_target == target_path, f"Symlink {link_path} points to {actual_target}, expected {target_path}."

def test_summary_log():
    log_path = "/home/user/summary.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) == 3, f"Summary log must contain exactly 3 lines, found {len(lines)}."
    assert lines[0] == "3", f"Line 1 of summary log should be '3', found '{lines[0]}'."
    assert lines[1] == "3", f"Line 2 of summary log should be '3', found '{lines[1]}'."
    assert lines[2] == "3", f"Line 3 of summary log should be '3', found '{lines[2]}'."