# test_final_state.py

import os
import tarfile

def test_c_program_exists_and_contains_functions():
    c_file_path = "/home/user/process_configs.c"
    assert os.path.exists(c_file_path), f"C program source file not found at {c_file_path}"
    assert os.path.isfile(c_file_path), f"{c_file_path} is not a file"

    with open(c_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for func in ["fread", "rename", "remove"]:
        assert func in content, f"C program must use the '{func}' function."

def test_updated_configs_archive_contents():
    archive_path = "/home/user/updated_configs.tar.gz"
    assert os.path.exists(archive_path), f"Final archive not found at {archive_path}"
    assert os.path.isfile(archive_path), f"{archive_path} is not a file"
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive"

    expected_files = {
        "plugin_alpha.elf",
        "plugin_beta.elf",
        "db_tx_1.wal",
        "db_tx_2.wal"
    }

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()

        # Ensure that paths are at the root (no directories)
        for name in names:
            assert "/" not in name, f"File '{name}' should be at the root of the archive, not in a directory."

        actual_files = set(names)

        missing = expected_files - actual_files
        extra = actual_files - expected_files

        assert not missing, f"Missing expected files in archive: {missing}"
        assert not extra, f"Unexpected files found in archive: {extra}"

def test_configs_directory_state():
    configs_dir = "/home/user/configs"
    if os.path.exists(configs_dir):
        files = os.listdir(configs_dir)
        # The unknown_blob should be deleted, and others renamed
        assert "unknown_blob" not in files, "The file 'unknown_blob' was not deleted from the configs directory."