# test_final_state.py
import os
import tarfile
import re

def test_valid_files_txt():
    txt_path = "/home/user/valid_files.txt"
    assert os.path.exists(txt_path), f"File {txt_path} does not exist."

    with open(txt_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {"data_alpha.dat 1024", "data_beta.dat 2048"}
    actual_lines = set(lines)

    assert actual_lines == expected_lines, f"Expected lines {expected_lines}, but got {actual_lines}"

def test_parser_c_locking():
    c_path = "/home/user/parser.c"
    assert os.path.exists(c_path), f"Source file {c_path} does not exist."

    with open(c_path, "r") as f:
        content = f.read()

    has_lock = re.search(r'\b(flock|fcntl)\s*\(', content)
    assert has_lock, f"The C program {c_path} does not appear to use flock() or fcntl() for file locking."

def test_clean_backup_tar():
    tar_path = "/home/user/clean_backup.tar"
    assert os.path.exists(tar_path), f"Backup tarball {tar_path} does not exist."
    assert tarfile.is_tarfile(tar_path), f"File {tar_path} is not a valid tar file."

    with tarfile.open(tar_path, "r") as tar:
        names = tar.getnames()

    expected_names = {"data_alpha.dat", "data_beta.dat"}
    actual_names = set(names)

    assert actual_names == expected_names, f"Expected tarball contents {expected_names}, but got {actual_names}"