# test_final_state.py

import os

def test_symlink_untouched():
    cycle_path = "/home/user/configs/cycle"
    assert os.path.islink(cycle_path), f"Symlink {cycle_path} was modified or deleted. It must remain a symlink."
    assert os.readlink(cycle_path) == "/home/user/configs", f"Symlink {cycle_path} target changed."

def test_c_code_modified():
    c_path = "/home/user/config_archiver.c"
    assert os.path.isfile(c_path), f"Source file {c_path} is missing."
    with open(c_path, "r") as f:
        content = f.read()
    assert "lstat" in content, "The C code does not appear to use lstat() as required to detect symlinks."

def test_archive_created_and_correct():
    archive_path = "/home/user/backup.rle"
    assert os.path.isfile(archive_path), f"Archive file {archive_path} was not created."

    with open(archive_path, "rb") as f:
        content = f.read()

    app_rle = b"\x0aA\x0aB\x0aC"
    db_rle = b"\x051\x052\x053\x054"

    valid_outputs = [
        app_rle + db_rle,
        db_rle + app_rle
    ]

    assert content in valid_outputs, (
        f"Archive content is incorrect. Expected one of the valid RLE combinations, but got: {content!r}"
    )