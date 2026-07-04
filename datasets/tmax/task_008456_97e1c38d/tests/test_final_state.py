# test_final_state.py

import os
import tarfile
import pytest

def test_project_directory_exists():
    assert os.path.isdir("/home/user/project"), "The /home/user/project/ directory does not exist."

def test_backup_full_exists_and_valid():
    backup_path = "/home/user/backup_full.tar.gz"
    assert os.path.isfile(backup_path), f"{backup_path} does not exist."
    assert tarfile.is_tarfile(backup_path), f"{backup_path} is not a valid tar archive."

def test_backup_snar_exists():
    snar_path = "/home/user/backup.snar"
    assert os.path.isfile(snar_path), f"{snar_path} does not exist."

def test_process_cpp_and_executable_exist():
    assert os.path.isfile("/home/user/process.cpp"), "/home/user/process.cpp does not exist."
    assert os.path.isfile("/home/user/process"), "/home/user/process executable does not exist."
    assert os.access("/home/user/process", os.X_OK), "/home/user/process is not executable."

def test_converted_files_content():
    core_module = "/home/user/project/core_module.cpp"
    utils_strings = "/home/user/project/utils_strings.cpp"

    assert os.path.isfile(core_module), f"{core_module} does not exist."
    assert os.path.isfile(utils_strings), f"{utils_strings} does not exist."

    with open(core_module, "rb") as f:
        core_content = f.read()

    with open(utils_strings, "rb") as f:
        utils_content = f.read()

    expected_core = b"/* Initialisation de la m\xc3\xa9moire */\nint main() { return 0; }\n"
    expected_utils = b"/* A\xc3\xb1adir funcionalidad */\nvoid add() {}\n"

    # Allow for missing trailing newline if the student's C++ program stripped it
    assert core_content.strip() == expected_core.strip(), f"Content of {core_module} is incorrect or not valid UTF-8."
    assert utils_content.strip() == expected_utils.strip(), f"Content of {utils_strings} is incorrect or not valid UTF-8."

def test_old_files_deleted():
    assert not os.path.exists("/home/user/project/data_01.txt"), "data_01.txt was not deleted."
    assert not os.path.exists("/home/user/project/data_02.txt"), "data_02.txt was not deleted."

def test_backup_inc_exists_and_valid():
    backup_path = "/home/user/backup_inc.tar.gz"
    assert os.path.isfile(backup_path), f"{backup_path} does not exist."
    assert tarfile.is_tarfile(backup_path), f"{backup_path} is not a valid tar archive."

def test_completion_log():
    log_path = "/home/user/completion.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["core_module.cpp", "index.csv", "utils_strings.cpp"]
    assert lines == expected_lines, f"Contents of {log_path} do not match the expected sorted list of files."