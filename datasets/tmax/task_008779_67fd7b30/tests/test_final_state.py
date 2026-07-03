# test_final_state.py

import os
import subprocess
import tarfile
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_backup_manager():
    """Runs the student's Go program before running the tests."""
    go_file = "/home/user/backup_manager.go"
    assert os.path.isfile(go_file), f"The file {go_file} does not exist."

    # Run the Go program
    result = subprocess.run(
        ["go", "run", go_file],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Go program failed to execute. stderr: {result.stderr}"

def test_archive_created_and_contents():
    archive_path = "/home/user/archive.tar.gz"
    assert os.path.isfile(archive_path), f"Archive file {archive_path} was not created."

    expected_files = {"app1/main.go", "app3/handlers.go"}

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            archived_names = set(tar.getnames())
    except tarfile.ReadError:
        pytest.fail(f"File {archive_path} is not a valid gzip-compressed tarball.")

    assert archived_names == expected_files, (
        f"Archive contents do not match expected files.\n"
        f"Expected: {expected_files}\n"
        f"Found: {archived_names}"
    )

def test_archived_files_txt():
    txt_path = "/home/user/archived_files.txt"
    assert os.path.isfile(txt_path), f"Text file {txt_path} was not created."

    expected_lines = {
        "/home/user/projects/app1/main.go",
        "/home/user/projects/app3/handlers.go"
    }

    with open(txt_path, "r") as f:
        # Read lines, strip whitespace/newlines, and ignore empty lines
        lines = {line.strip() for line in f if line.strip()}

    assert lines == expected_lines, (
        f"Contents of {txt_path} do not match expected paths.\n"
        f"Expected: {expected_lines}\n"
        f"Found: {lines}"
    )