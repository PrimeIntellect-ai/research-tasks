# test_final_state.py
import os
import tarfile
import pytest

def test_source_and_executable_exist():
    assert os.path.exists("/home/user/curator.c"), "Source file /home/user/curator.c is missing."
    assert os.path.exists("/home/user/curator"), "Executable /home/user/curator is missing."
    assert os.access("/home/user/curator", os.X_OK), "/home/user/curator is not executable."

def test_curated_archive_exists_and_valid():
    archive_path = "/home/user/curated/artifact_curated.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} is missing."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()
        # Should contain only sys_report.log (possibly inside a directory, but no binary_data.bin)
        log_files = [m for m in members if m.endswith("sys_report.log")]
        bin_files = [m for m in members if m.endswith("binary_data.bin")]

        assert len(log_files) == 1, f"Expected exactly one sys_report.log in archive, found: {log_files}"
        assert len(bin_files) == 0, f"Archive should not contain binary_data.bin, but found: {bin_files}"

        # Check content of sys_report.log
        f = tar.extractfile(log_files[0])
        assert f is not None, "Could not extract sys_report.log from archive."
        content = f.read()

        try:
            text_content = content.decode('utf-8')
        except UnicodeDecodeError:
            pytest.fail("sys_report.log in archive is not valid UTF-8.")

        expected_text = "System boot sequence initiated.\nError 0x44: Legacy module failed."
        assert expected_text in text_content.replace('\r\n', '\n'), "The converted log file does not contain the expected text."

def test_summary_file():
    summary_path = "/home/user/curated/summary.txt"
    assert os.path.exists(summary_path), f"Summary file {summary_path} is missing."

    with open(summary_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "sys_report.log" in content, "summary.txt does not contain the processed log file name."