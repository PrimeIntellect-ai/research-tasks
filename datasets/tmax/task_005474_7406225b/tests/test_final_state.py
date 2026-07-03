# test_final_state.py
import os
import pytest

def test_cpp_source_and_binary():
    cpp_path = "/home/user/art_tool.cpp"
    bin_path = "/home/user/art_tool"

    assert os.path.isfile(cpp_path), f"C++ source code {cpp_path} is missing."
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."

    with open(cpp_path, "r", encoding="utf-8") as f:
        content = f.read()

    has_fcntl_include = "<fcntl.h>" in content or "<sys/file.h>" in content
    assert has_fcntl_include, "C++ source does not include <fcntl.h> or <sys/file.h> for file locking."

    has_lock_call = "flock" in content or "F_SETLKW" in content or "F_SETLK" in content
    assert has_lock_call, "C++ source does not contain 'flock' or 'F_SETLKW'/'F_SETLK' for file locking."

def test_extracted_file():
    target_file = "/home/user/out_files/file1.txt"
    assert os.path.isfile(target_file), f"Extracted file {target_file} is missing."

    with open(target_file, "rb") as f:
        content = f.read()

    expected_content = b"Hello World! This is a test."
    assert content == expected_content, f"File content mismatch. Expected {expected_content}, got {content}"

def test_symlinks_and_cycle_log():
    out_dir = "/home/user/out_files"
    valid_link = os.path.join(out_dir, "valid_link")

    assert os.path.islink(valid_link), f"Symlink {valid_link} is missing or not a symlink."
    assert os.readlink(valid_link) == "file1.txt", f"Symlink {valid_link} does not point to 'file1.txt'."

    cycle_links = ["linkA", "linkB", "linkC"]
    existing_links = []
    missing_links = []

    for link in cycle_links:
        link_path = os.path.join(out_dir, link)
        if os.path.islink(link_path):
            existing_links.append(link)
        else:
            missing_links.append(link)

    assert len(missing_links) >= 1, "A cycle was created! None of the cyclic symlinks were prevented."
    assert len(missing_links) == 1, f"Expected exactly 1 symlink to be rejected to break the cycle, but {len(missing_links)} are missing: {missing_links}"

    log_file = "/home/user/cycle_log.txt"
    assert os.path.isfile(log_file), f"Cycle log file {log_file} is missing."

    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read().strip().splitlines()

    rejected_link = missing_links[0]
    assert any(rejected_link in line for line in log_content), f"Cycle log does not contain the rejected symlink '{rejected_link}'."