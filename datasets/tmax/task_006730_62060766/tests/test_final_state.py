# test_final_state.py
import os
import pytest

def test_repo_files_exist_and_content():
    repo_dir = "/home/user/repo"

    file1 = os.path.join(repo_dir, "CORE_b10a8db164e0754105b7a99be72e3fe5.bin")
    file2 = os.path.join(repo_dir, "CORE_70db6bfbe5a8c2ba42718cd99818817a.bin")

    assert os.path.isfile(file1), f"Expected file {file1} does not exist. The payload was not extracted or the filename is incorrect."
    assert os.path.isfile(file2), f"Expected file {file2} does not exist. The payload was not extracted or the filename is incorrect."

    with open(file1, "rb") as f:
        content1 = f.read()
    assert content1 == b"Hello World", f"Content of {file1} is incorrect. Expected 'Hello World', got {content1}"

    with open(file2, "rb") as f:
        content2 = f.read()
    assert content2 == b"Valid Payload 2", f"Content of {file2} is incorrect. Expected 'Valid Payload 2', got {content2}"

def test_no_extra_bin_files():
    repo_dir = "/home/user/repo"
    if not os.path.exists(repo_dir):
        pytest.fail(f"Directory {repo_dir} does not exist.")

    bin_files = [f for f in os.listdir(repo_dir) if f.endswith(".bin")]

    assert len(bin_files) == 2, f"Expected exactly 2 .bin files in {repo_dir}, but found {len(bin_files)}: {bin_files}"

def test_summary_file():
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"Summary file {summary_path} does not exist."

    with open(summary_path, "r") as f:
        content = f.read().strip()

    assert content == "2", f"Summary file content is incorrect. Expected '2', got '{content}'"