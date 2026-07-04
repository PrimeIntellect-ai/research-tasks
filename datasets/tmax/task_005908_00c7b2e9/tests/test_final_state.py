# test_final_state.py

import os
import tarfile

def test_c_source_file_exists():
    c_file = "/home/user/filter_logs.c"
    assert os.path.isfile(c_file), f"The C source file {c_file} is missing."

def test_executable_exists_and_is_executable():
    executable = "/home/user/filter_logs"
    assert os.path.isfile(executable), f"The executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"The file {executable} is not executable."

def test_cleaned_log_content():
    output_log = "/home/user/cleaned_server_01.log"
    assert os.path.isfile(output_log), f"The output log {output_log} is missing."

    expected_content = (
        "[INFO] System boot sequence initiated.\n"
        "[INFO] Volumes mounted successfully.\n"
        "[ERROR] Disk quota exceeded ERROR_CODE:000\n"
        "[INFO] Cleanup yielded 500MB.\n"
        "[ERROR] Database sync failed ERROR_CODE:000\n"
        "[INFO] System running.\n"
    )

    with open(output_log, "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, (
        f"The content of {output_log} does not match the expected output. "
        f"Actual content:\n{actual_content}"
    )

def test_original_archive_untouched():
    archive_path = "/home/user/system_logs.tar.gz"
    assert os.path.isfile(archive_path), f"The original archive {archive_path} is missing."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()
            assert "server_01.log" in names, "The archive was modified and is missing 'server_01.log'."
    except tarfile.ReadError:
        assert False, f"The file {archive_path} is no longer a valid gzip tar archive."

def test_server_01_log_not_extracted_to_disk():
    log_path = "/home/user/server_01.log"
    assert not os.path.exists(log_path), (
        f"The file {log_path} exists on disk. You were supposed to process the file "
        "without extracting it to the disk first."
    )