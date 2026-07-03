# test_final_state.py

import os
import pytest

def test_extracted_texts_directory():
    dir_path = "/home/user/extracted_texts"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

    expected_files = ["alpha_data.txt", "beta_data.txt", "gamma_data.txt"]
    for f in expected_files:
        file_path = os.path.join(dir_path, f)
        assert os.path.isfile(file_path), f"Expected file {f} is missing in {dir_path}."

def test_cleaned_texts_directory_and_contents():
    dir_path = "/home/user/cleaned_texts"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

    expected_contents = {
        "alpha_data.txt": "Experiment 1: [UPDATED_TAG] recorded at dawn.\n",
        "beta_data.txt": "[UPDATED_TAG] is no longer used. [UPDATED_TAG]\n",
        "gamma_data.txt": "Gamma results with [UPDATED_TAG] present.\n"
    }

    for filename, expected_text in expected_contents.items():
        file_path = os.path.join(dir_path, filename)
        assert os.path.isfile(file_path), f"Cleaned file {filename} is missing."

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            pytest.fail(f"File {filename} is not properly UTF-8 encoded.")

        assert content.strip() == expected_text.strip(), f"Content of {filename} is incorrect. Expected: {expected_text.strip()}, Got: {content.strip()}"

def test_final_dataset_symlinks():
    dir_path = "/home/user/final_dataset"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

    expected_files = ["alpha_data.txt", "beta_data.txt", "gamma_data.txt"]
    for f in expected_files:
        symlink_path = os.path.join(dir_path, f)
        assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

        target = os.readlink(symlink_path)
        expected_target = os.path.join("/home/user/cleaned_texts", f)
        assert target == expected_target, f"Symlink {f} points to {target} instead of {expected_target}."

def test_summary_log():
    log_path = "/home/user/summary.log"
    assert os.path.isfile(log_path), f"Summary log {log_path} does not exist."

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["alpha_data.txt", "beta_data.txt", "gamma_data.txt"]
    assert lines == expected_lines, f"Summary log contents are incorrect. Expected {expected_lines}, got {lines}."