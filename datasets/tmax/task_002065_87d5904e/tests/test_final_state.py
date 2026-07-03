# test_final_state.py

import os
import json
import pytest

def test_path_escapes_log():
    log_path = "/home/user/project_dir/path_escapes.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Invalid path escape attempt: ../database_backup.csv",
        "Invalid path escape attempt: conf/../../etc/passwd",
        "Invalid path escape attempt: src/nested/../../../app.py"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in log file, but found {len(lines)}."
    for expected in expected_lines:
        assert expected in lines, f"Missing expected log entry: '{expected}'"

def test_valid_symlinks_created():
    workspace = "/home/user/project_dir/organized_workspace"
    source_dir = "/home/user/project_dir/source_files"

    # Check src/app.py
    app_py_link = os.path.join(workspace, "src/app.py")
    assert os.path.islink(app_py_link), f"{app_py_link} should be a symlink."
    assert os.readlink(app_py_link) == os.path.join(source_dir, "app.py"), f"{app_py_link} does not point to the correct source file."

    # Check data/db.csv
    db_csv_link = os.path.join(workspace, "data/db.csv")
    assert os.path.islink(db_csv_link), f"{db_csv_link} should be a symlink."
    assert os.readlink(db_csv_link) == os.path.join(source_dir, "database.csv"), f"{db_csv_link} does not point to the correct source file."

def test_valid_hardlinks_created():
    workspace = "/home/user/project_dir/organized_workspace"
    source_dir = "/home/user/project_dir/source_files"

    # Check assets/style.css
    style_css_link = os.path.join(workspace, "assets/style.css")
    style_css_src = os.path.join(source_dir, "style.css")

    assert os.path.isfile(style_css_link), f"{style_css_link} should exist."
    assert not os.path.islink(style_css_link), f"{style_css_link} should be a hardlink, not a symlink."

    # Check if they point to the same inode
    assert os.stat(style_css_link).st_ino == os.stat(style_css_src).st_ino, f"{style_css_link} is not a hardlink to {style_css_src}."

def test_escaped_files_not_created():
    project_dir = "/home/user/project_dir"

    escaped_files = [
        "database_backup.csv",
        "app.py"
    ]

    for f in escaped_files:
        path = os.path.join(project_dir, f)
        assert not os.path.exists(path), f"Escaped file {path} should not have been created."

    # Also check /home/user/etc/passwd or similar if it was evaluated relative to project_dir
    # The prompt explicitly mentions /home/user/project_dir/database_backup.csv should not exist.