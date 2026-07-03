# test_final_state.py

import os
import re
import stat

def test_count_txt():
    count_path = "/home/user/count.txt"
    assert os.path.isfile(count_path), f"File {count_path} does not exist."

    with open(count_path, "r") as f:
        content = f.read().strip()

    assert content == "2", f"Expected count.txt to contain '2', but got '{content}'."

def test_critical_archive_log():
    archive_path = "/home/user/critical_archive.log"
    assert os.path.isfile(archive_path), f"File {archive_path} does not exist."

    expected_content = """[2023-10-25 14:05:00] CRITICAL Disk space exhausted:
Volume /dev/sda1 has 0 bytes left.
Please free up space immediately.
[2023-10-25 14:10:00] CRITICAL Database connection lost:
Error 104: Connection reset by peer
Stack trace:
  at db_connect()
  at main()
"""

    with open(archive_path, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), "The content of critical_archive.log does not match the expected output."

def test_tmp_file_not_exists():
    tmp_path = "/home/user/critical_archive.log.tmp"
    assert not os.path.exists(tmp_path), f"Temporary file {tmp_path} should not exist (it should have been renamed)."

def test_archiver_cpp_contains_rename():
    cpp_path = "/home/user/archiver.cpp"
    assert os.path.isfile(cpp_path), f"Source file {cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        content = f.read()

    assert re.search(r'\brename\s*\(', content), f"The word 'rename' (or 'std::rename') was not found as a function call in {cpp_path}."

def test_archiver_executable():
    exe_path = "/home/user/archiver"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."