# test_final_state.py

import os
import subprocess
import tarfile
import pytest

def test_archiver_binary_exists():
    assert os.path.isfile("/home/user/archiver"), "The Go binary /home/user/archiver does not exist."
    assert os.access("/home/user/archiver", os.X_OK), "The Go binary /home/user/archiver is not executable."

def test_adversarial_corpus_clean():
    clean_dir = "/app/corpus/clean/"
    result = subprocess.run(["/home/user/archiver", clean_dir], capture_output=True, text=True)
    output = result.stdout + "\n" + result.stderr

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".conf")]
    bypassed = []

    for f in clean_files:
        expected_str = f"ACCEPTED: {f}"
        if expected_str not in output:
            bypassed.append(f)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(bypassed)}")

def test_adversarial_corpus_evil():
    evil_dir = "/app/corpus/evil/"
    result = subprocess.run(["/home/user/archiver", evil_dir], capture_output=True, text=True)
    output = result.stdout + "\n" + result.stderr

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".conf")]
    bypassed = []

    for f in evil_files:
        expected_str = f"REJECTED: {f}"
        if expected_str not in output:
            bypassed.append(f)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}")

def test_final_archive_exists_and_correct():
    archive_path = "/home/user/final_backup_omega.tar.gz"
    assert os.path.isfile(archive_path), f"Final archive missing: {archive_path}"

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()
        conf_files = [m for m in members if m.endswith(".conf")]

        assert len(conf_files) == 2, f"Archive should contain exactly 2 .conf files, found {len(conf_files)}"

        expected_basenames = {"server1.conf", "server2.conf"}
        actual_basenames = {os.path.basename(m) for m in conf_files}
        assert expected_basenames.issubset(actual_basenames), f"Archive missing expected files. Found: {actual_basenames}"

        for m in conf_files:
            f = tar.extractfile(m)
            content = f.read().decode("utf-8")
            assert "DEBUG_LEVEL=1" in content, f"File {m} in archive was not properly transformed. Content: {content}"
            assert "DEBUG_LEVEL=0" not in content, f"File {m} in archive still contains DEBUG_LEVEL=0."