# test_final_state.py

import os
import tarfile
import pytest

def test_go_program_exists_and_uses_flock():
    go_file = "/home/user/processor.go"
    assert os.path.isfile(go_file), f"{go_file} does not exist."
    with open(go_file, "r") as f:
        content = f.read()

    # Check for Flock usage
    assert "Flock" in content, "The Go program must use file locking (e.g., syscall.Flock)."

def test_redaction_index_log():
    index_file = "/home/user/redaction_index.log"
    assert os.path.isfile(index_file), f"{index_file} does not exist."

    with open(index_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "1.txt,2",
        "2.txt,0",
        "3.txt,1",
        "4.txt,3"
    }

    actual_lines = set(lines)
    assert actual_lines == expected_lines, f"Expected index lines {expected_lines}, but got {actual_lines}"
    assert len(lines) == 4, "The index file should contain exactly 4 lines."

def test_processed_logs_archive():
    archive_path = "/home/user/processed_logs.tar.gz"
    assert os.path.isfile(archive_path), f"{archive_path} does not exist."

    expected_suffixes = {
        "Apollo/1.txt",
        "Apollo/3.txt",
        "Gemini/2.txt",
        "Artemis/4.txt"
    }

    found_suffixes = set()

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()
        for member in members:
            if member.isfile():
                for suffix in expected_suffixes:
                    if member.name.endswith(suffix):
                        found_suffixes.add(suffix)

                        # Check content of 1.txt
                        if suffix == "Apollo/1.txt":
                            f = tar.extractfile(member)
                            content = f.read().decode("utf-8")
                            assert "[REDACTED]" in content, "1.txt does not contain [REDACTED]"
                            assert "192.168.1.15" not in content, "1.txt still contains 192.168.1.15"
                            assert "10.0.0.2" not in content, "1.txt still contains 10.0.0.2"

                        # Check content of 4.txt
                        if suffix == "Artemis/4.txt":
                            f = tar.extractfile(member)
                            content = f.read().decode("utf-8")
                            assert "8.8.8.8" not in content, "4.txt still contains 8.8.8.8"
                            assert "127.0.0.1" not in content, "4.txt still contains 127.0.0.1"
                            assert content.count("[REDACTED]") == 3, "4.txt should have 3 redactions"

    assert found_suffixes == expected_suffixes, f"Archive is missing some required files. Found: {found_suffixes}"

def test_organized_logs_directory_structure():
    base_dir = "/home/user/organized_logs"
    assert os.path.isdir(base_dir), f"{base_dir} does not exist."

    expected_files = {
        "Apollo/1.txt",
        "Apollo/3.txt",
        "Gemini/2.txt",
        "Artemis/4.txt"
    }

    for rel_path in expected_files:
        full_path = os.path.join(base_dir, rel_path)
        assert os.path.isfile(full_path), f"Expected file {full_path} is missing from organized_logs."