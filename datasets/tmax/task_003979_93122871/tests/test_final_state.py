# test_final_state.py
import os

def test_processed_logs_directory_exists():
    path = "/home/user/processed_logs"
    assert os.path.isdir(path), f"Directory {path} does not exist."

def test_processed_files_exist_and_content_is_utf8():
    expected_files = {
        "1001.txt": "ARCHIVE-ID: 1001\nSystem status: échoué\n",
        "2005.txt": "ARCHIVE-ID: 2005\nTemperature: 45°C\n",
        "99X3.txt": "ARCHIVE-ID: 99X3\nUser: mädchen\n"
    }

    for filename, expected_content in expected_files.items():
        filepath = os.path.join("/home/user/processed_logs", filename)
        assert os.path.isfile(filepath), f"File {filepath} does not exist."

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        assert content == expected_content, f"Content of {filepath} does not match expected UTF-8 content. Got: {repr(content)}"

def test_processed_manifest_exists_and_correct():
    path = "/home/user/processed_manifest.txt"
    assert os.path.isfile(path), f"Manifest file {path} does not exist."

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = ["1001.txt", "2005.txt", "99X3.txt"]
    assert lines == expected_lines, f"Manifest file content does not match. Expected {expected_lines}, got {lines}"

def test_original_archive_exists():
    path = "/home/user/legacy_backups.tar.gz"
    assert os.path.isfile(path), f"Original archive {path} was deleted or is not a file."