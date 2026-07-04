# test_final_state.py

import os

def test_published_docs_directory_exists():
    dir_path = "/home/user/published_docs"
    assert os.path.exists(dir_path), f"The directory {dir_path} does not exist."
    assert os.path.isdir(dir_path), f"The path {dir_path} is not a directory."

def test_published_docs_files_and_contents():
    expected_files = {
        "section_01.md": "Welcome to [PUBLIC_RELEASE] part 1.",
        "section_02.md": "Advanced routing in [PUBLIC_RELEASE] part 2.",
        "section_03.md": "Troubleshooting the [PUBLIC_RELEASE] system."
    }

    dir_path = "/home/user/published_docs"

    for filename, expected_content in expected_files.items():
        file_path = os.path.join(dir_path, filename)
        assert os.path.exists(file_path), f"The file {file_path} is missing."
        assert os.path.isfile(file_path), f"The path {file_path} is not a file."

        with open(file_path, "r") as f:
            content = f.read()
            assert content == expected_content, f"Content of {file_path} is incorrect. Expected '{expected_content}', got '{content}'."

def test_migration_log():
    log_path = "/home/user/migration_log.txt"
    assert os.path.exists(log_path), f"The log file {log_path} does not exist."
    assert os.path.isfile(log_path), f"The path {log_path} is not a file."

    expected_lines = [
        "/home/user/published_docs/section_01.md",
        "/home/user/published_docs/section_02.md",
        "/home/user/published_docs/section_03.md"
    ]

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == expected_lines, f"The contents of {log_path} are incorrect. Expected {expected_lines}, got {lines}."