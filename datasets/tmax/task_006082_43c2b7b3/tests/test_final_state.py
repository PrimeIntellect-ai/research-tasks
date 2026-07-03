# test_final_state.py

import os
import tarfile

def test_to_delete_log_contents():
    log_path = "/home/user/to_delete.log"
    assert os.path.isfile(log_path), f"Expected log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "/home/user/backups/proj_alpha/test1.gz",
        "/home/user/backups/proj_beta/old/core.gz"
    ]

    assert lines == expected_lines, f"Contents of {log_path} are incorrect. Expected {expected_lines}, got {lines}."

def test_cleanup_tar_exists_and_contents():
    tar_path = "/home/user/cleanup.tar"
    assert os.path.isfile(tar_path), f"Expected tar archive {tar_path} does not exist."

    with tarfile.open(tar_path, "r") as tar:
        members = tar.getmembers()
        # Should only contain to_delete.log
        filenames = [m.name for m in members]

        assert "to_delete.log" in filenames, "The tar file must contain 'to_delete.log'."
        assert len(filenames) == 1, f"The tar file should only contain one file, but contains: {filenames}"

        # Extract and verify contents
        f = tar.extractfile("to_delete.log")
        assert f is not None, "Could not extract 'to_delete.log' from tar file."

        content = f.read().decode("utf-8").strip().split("\n")
        lines = [line.strip() for line in content if line.strip()]

        expected_lines = [
            "/home/user/backups/proj_alpha/test1.gz",
            "/home/user/backups/proj_beta/old/core.gz"
        ]

        assert lines == expected_lines, f"Contents of to_delete.log inside the tar file are incorrect. Expected {expected_lines}, got {lines}."