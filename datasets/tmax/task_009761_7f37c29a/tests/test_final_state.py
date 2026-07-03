# test_final_state.py

import os
import tarfile
import pytest

def test_tar_file_exists_and_contents():
    tar_path = "/home/user/vuln_backup.tar"
    assert os.path.exists(tar_path), f"Tar file {tar_path} does not exist."

    with tarfile.open(tar_path, "r") as tar:
        names = tar.getnames()

        # Check config.txt
        assert "config.txt" in names, "config.txt is missing from the tar archive."
        f_config = tar.extractfile("config.txt")
        assert f_config is not None, "config.txt is not a regular file."
        assert f_config.read().decode('utf-8').strip() == "SAFE_MODE=1", "Incorrect content for config.txt."

        # Check config_link.txt
        assert "config_link.txt" in names, "config_link.txt is missing from the tar archive."
        link_member = tar.getmember("config_link.txt")
        assert link_member.issym(), "config_link.txt is not a symbolic link."
        assert link_member.linkname == "config.txt", "config_link.txt does not point to config.txt."

        # Check ../pwned.txt
        assert "../pwned.txt" in names, "../pwned.txt is missing from the tar archive."
        f_pwned = tar.extractfile("../pwned.txt")
        assert f_pwned is not None, "../pwned.txt is not a regular file."
        assert f_pwned.read().decode('utf-8').strip() == "YOU_HAVE_BEEN_COMPROMISED", "Incorrect content for ../pwned.txt."

def test_log_file_exists_and_contents():
    log_path = "/home/user/archive_list.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r", encoding="utf-8") as log:
        content = log.read()
        assert "config.txt" in content, "Log file is missing entry for config.txt."
        assert "config_link.txt" in content, "Log file is missing entry for config_link.txt."
        assert "../pwned.txt" in content, "Log file is missing entry for ../pwned.txt."

def test_python_script_exists():
    script_path = "/home/user/make_test_tar.py"
    assert os.path.exists(script_path), f"Python script {script_path} does not exist."