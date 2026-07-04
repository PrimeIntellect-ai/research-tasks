# test_final_state.py
import os
import pytest

BASE_DIR = "/home/user/legacy_docs"
LOG_FILE = "/home/user/migration_log.csv"

FILES = [
    {
        "original_path": "drafts/overview.txt",
        "expected_name": "2020-05-12_overview.txt",
        "expected_utf8": "L’histoire de la bête",
    },
    {
        "original_path": "published/v1/api_specs.txt",
        "expected_name": "2018-11-23_api_specs.txt",
        "expected_utf8": "Méthodes et propriétés",
    },
    {
        "original_path": "readme.txt",
        "expected_name": "2023-01-02_readme.txt",
        "expected_utf8": "Copyright © 2023",
    }
]

def test_original_files_removed():
    for f in FILES:
        old_path = os.path.join(BASE_DIR, f["original_path"])
        assert not os.path.exists(old_path), f"Original file {old_path} should have been renamed/removed."

def test_new_files_exist_and_utf8_content():
    for f in FILES:
        dir_name = os.path.dirname(f["original_path"])
        new_path = os.path.join(BASE_DIR, dir_name, f["expected_name"])

        assert os.path.exists(new_path), f"Expected renamed file does not exist: {new_path}"

        with open(new_path, "rb") as file_obj:
            content_bytes = file_obj.read()

        try:
            content_str = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail(f"File {new_path} is not valid UTF-8.")

        assert content_str == f["expected_utf8"], f"Content of {new_path} does not match expected UTF-8 text."

def test_migration_log_csv():
    assert os.path.exists(LOG_FILE), f"Migration log {LOG_FILE} is missing."

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = []
    for f in FILES:
        old_path = os.path.join(BASE_DIR, f["original_path"])
        dir_name = os.path.dirname(f["original_path"])
        new_path = os.path.join(BASE_DIR, dir_name, f["expected_name"])
        expected_lines.append(f"{old_path},{new_path}")

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in log file, but found {len(lines)}."

    for expected_line in expected_lines:
        assert expected_line in lines, f"Expected line '{expected_line}' not found in {LOG_FILE}."