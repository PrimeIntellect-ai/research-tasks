# test_final_state.py

import os
import tarfile
import pytest

def test_c_program_exists():
    assert os.path.isfile("/home/user/curator.c"), "The C program /home/user/curator.c is missing."

def test_c_binary_exists_and_executable():
    assert os.path.isfile("/home/user/curator"), "The compiled binary /home/user/curator is missing."
    assert os.access("/home/user/curator", os.X_OK), "The binary /home/user/curator is not executable."

def test_bash_script_exists_and_executable():
    script_path = "/home/user/process_and_backup.sh"
    assert os.path.isfile(script_path), f"The bash script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"The bash script {script_path} is not executable."

def test_curated_artifacts_csv():
    csv_path = "/home/user/curated_artifacts.csv"
    assert os.path.isfile(csv_path), f"The output file {csv_path} is missing."

    with open(csv_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "BIN-001,Initial release résumé",
        "BIN-002,Patch update",
        "BIN-003,Secürity fix",
        "BIN-004,Deprecated"
    ]

    assert sorted(lines) == sorted(expected_lines), f"The contents of {csv_path} do not match the expected output."

def test_backup_exists_and_valid():
    backup_path = "/home/user/backups/csv_backup.tar.gz"
    assert os.path.isfile(backup_path), f"The backup file {backup_path} is missing."

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            # Check if the csv file is in the tar archive (could be absolute or relative path)
            assert any(name.endswith("curated_artifacts.csv") for name in names), "The backup archive does not contain curated_artifacts.csv."
    except tarfile.TarError:
        pytest.fail(f"The file {backup_path} is not a valid tar.gz archive.")