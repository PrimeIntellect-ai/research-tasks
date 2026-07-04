# test_final_state.py
import os
import tarfile
import pytest

def test_gcode_time_log():
    log_path = "/home/user/gcode_time.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == "Total Print Time: 7700", f"Log file content is incorrect. Expected 'Total Print Time: 7700', got '{content}'."

def test_tarball_exists_and_contents():
    tar_path = "/home/user/safe_backup.tar.gz"
    assert os.path.exists(tar_path), f"Tarball {tar_path} does not exist."
    assert tarfile.is_tarfile(tar_path), f"File {tar_path} is not a valid tar archive."

    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getnames()

        for member in members:
            assert "loop_link" not in member, f"Symlink loop_link should not be in the archive, found: {member}"
            assert "research_data" not in member, f"Nested research_data should not be in the archive, found: {member}"

        expected_files = [
            "experiment1/meta.txt",
            "experiment1/run.gcode",
            "experiment2/meta.txt",
            "experiment2/run.gcode"
        ]

        found_files = set()
        for member in members:
            for exp in expected_files:
                if member.endswith(exp):
                    found_files.add(exp)

        missing = set(expected_files) - found_files
        assert not missing, f"Missing expected files in tarball: {missing}"

def test_tarball_meta_files_utf8():
    tar_path = "/home/user/safe_backup.tar.gz"
    assert os.path.exists(tar_path), f"Tarball {tar_path} does not exist."

    with tarfile.open(tar_path, "r:gz") as tar:
        for member in tar.getmembers():
            if member.name.endswith("experiment1/meta.txt"):
                f = tar.extractfile(member)
                assert f is not None, "Could not extract experiment1/meta.txt"
                try:
                    content = f.read().decode("utf-8")
                except UnicodeDecodeError:
                    pytest.fail("experiment1/meta.txt is not valid UTF-8.")
                assert "°" in content, "Missing '°' in experiment1/meta.txt"
                assert "Ü" in content, "Missing 'Ü' in experiment1/meta.txt"
            elif member.name.endswith("experiment2/meta.txt"):
                f = tar.extractfile(member)
                assert f is not None, "Could not extract experiment2/meta.txt"
                try:
                    content = f.read().decode("utf-8")
                except UnicodeDecodeError:
                    pytest.fail("experiment2/meta.txt is not valid UTF-8.")
                assert "é" in content, "Missing 'é' in experiment2/meta.txt"