# test_final_state.py

import os
import tarfile
import pytest

def test_doc_parser_c_exists():
    """Verify the C program was created."""
    assert os.path.exists("/home/user/doc_parser.c"), "The C program /home/user/doc_parser.c is missing."

def test_recovered_docs_dir_exists():
    """Verify the recovered_docs directory was created."""
    assert os.path.isdir("/home/user/recovered_docs"), "The directory /home/user/recovered_docs/ is missing."

def test_recovery_log():
    """Verify the recovery.log file contains the sorted filenames."""
    log_path = "/home/user/recovery.log"
    assert os.path.exists(log_path), f"The log file {log_path} is missing."

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "advanced_config.txt",
        "getting_started.txt",
        "troubleshooting.txt"
    ]
    assert lines == expected_lines, f"The contents of {log_path} do not match the expected sorted filenames."

def test_recovered_files_content_and_encoding():
    """Verify the recovered files exist, are UTF-8 encoded, and have correct content."""
    expected_files = {
        "getting_started.txt": "Welcome to the system.\nIt is very easy to use.\n© 2023 Corporation.\n",
        "advanced_config.txt": "Advanced settings:\n- Set proxy to 127.0.0.1\n- ¿Que pasa?\n",
        "troubleshooting.txt": "If it breaks, try turning it off and on.\nError æ is fatal.\n"
    }

    for filename, expected_content in expected_files.items():
        file_path = os.path.join("/home/user/recovered_docs", filename)
        assert os.path.exists(file_path), f"Recovered file missing: {file_path}"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            pytest.fail(f"File {file_path} is not valid UTF-8.")

        assert content == expected_content, f"Content of {file_path} does not match the expected UTF-8 text."

def test_clean_docs_tarball():
    """Verify the clean_docs.tar.gz exists and contains the recovered files."""
    tarball_path = "/home/user/clean_docs.tar.gz"
    assert os.path.exists(tarball_path), f"The tarball {tarball_path} is missing."

    assert tarfile.is_tarfile(tarball_path), f"{tarball_path} is not a valid tar archive."

    with tarfile.open(tarball_path, "r:gz") as tar:
        names = tar.getnames()

    # The tarball should contain the files directly or within a recovered_docs folder
    basenames = [os.path.basename(name) for name in names if not name.endswith('/')]

    expected_files = [
        "advanced_config.txt",
        "getting_started.txt",
        "troubleshooting.txt"
    ]

    for ef in expected_files:
        assert ef in basenames, f"File {ef} is missing from the tarball {tarball_path}."