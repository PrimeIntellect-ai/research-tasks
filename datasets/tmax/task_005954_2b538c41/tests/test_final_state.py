# test_final_state.py

import os
import tarfile
import pytest

def test_new_docs_files_and_contents():
    expected_files = {
        "/home/user/new_docs/System_Overview/introduction.txt": "Welcome to the GlobalTech system docs.\n",
        "/home/user/new_docs/API_Reference/authentication.txt": "The GlobalTech API is RESTful.\n",
        "/home/user/new_docs/User_Guides/routing_setup.txt": "GlobalTech guide to routing.\n"
    }

    for path, expected_content in expected_files.items():
        assert os.path.isfile(path), f"Expected file {path} was not created."
        with open(path, "r") as f:
            content = f.read()
            assert content.strip() == expected_content.strip(), f"Content of {path} is incorrect. Expected '{expected_content.strip()}', got '{content.strip()}'."

def test_release_tarball():
    tar_path = "/home/user/release.tar.gz"
    assert os.path.isfile(tar_path), f"Tarball {tar_path} was not created."

    with tarfile.open(tar_path, "r:gz") as tar:
        names = tar.getnames()
        # The tarball should contain new_docs at its root
        expected_entries = [
            "new_docs/System_Overview/introduction.txt",
            "new_docs/API_Reference/authentication.txt",
            "new_docs/User_Guides/routing_setup.txt"
        ]

        # Check that the required files are present in the tarball
        # Note: tar getnames might include leading './' depending on how it was created,
        # so we check if the path ends with the expected entry.
        for expected in expected_entries:
            found = any(name.endswith(expected) for name in names)
            assert found, f"Expected file {expected} not found in tarball {tar_path}."

def test_migration_log():
    log_path = "/home/user/migration.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "authentication.txt",
        "introduction.txt",
        "routing_setup.txt"
    ]

    assert lines == expected_lines, f"Log file contents incorrect. Expected {expected_lines}, got {lines}."

def test_ignored_file_not_processed():
    # Ensure that ignore_me.txt.gz was not processed
    # We can check if any file contains its text
    for root, dirs, files in os.walk("/home/user/new_docs"):
        for file in files:
            with open(os.path.join(root, file), "r") as f:
                content = f.read()
                assert "Ignore this file" not in content, f"Ignored file content found in {file}."