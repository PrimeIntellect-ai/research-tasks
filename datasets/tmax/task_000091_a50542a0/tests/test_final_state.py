# test_final_state.py

import os
import tarfile
import subprocess
import pytest

def test_final_docs_archive_exists_and_correct():
    archive_path = "/home/user/final_docs.tar.gz"
    assert os.path.isfile(archive_path), f"Missing archive: {archive_path}"

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()

        # Check for release_v2 directory
        has_release_v2 = any(m.name.endswith("release_v2") and m.isdir() for m in members)
        assert has_release_v2, "Missing 'release_v2' directory in archive."

        # Check for index.json hard link
        index_json_member = next((m for m in members if m.name.endswith("release_v2/index.json")), None)
        assert index_json_member is not None, "Missing 'index.json' in release_v2."
        # Note: tarfile handles hard links, but its representation might depend on how it was archived.
        # We at least ensure the file exists in the correct structure.

        # Check for symlink attachments/firmware.elf -> bin/main.elf
        symlink_member = next((m for m in members if m.name.endswith("attachments/firmware.elf")), None)
        assert symlink_member is not None, "Missing 'attachments/firmware.elf' in archive."
        assert symlink_member.issym(), "attachments/firmware.elf is not a symlink."
        assert symlink_member.linkname == "bin/main.elf" or symlink_member.linkname.endswith("bin/main.elf"), \
            f"Symlink points to wrong target: {symlink_member.linkname}"

def test_sanitizer_exists():
    script_path = "/home/user/sanitizer.py"
    assert os.path.isfile(script_path), f"Missing sanitizer script: {script_path}"

def test_sanitizer_clean_corpus():
    script_path = "/home/user/sanitizer.py"
    clean_corpus_dir = "/app/corpus/clean"

    assert os.path.isdir(clean_corpus_dir), "Clean corpus directory missing."

    clean_subdirs = [os.path.join(clean_corpus_dir, d) for d in os.listdir(clean_corpus_dir) 
                     if os.path.isdir(os.path.join(clean_corpus_dir, d))]

    failed_clean = []
    for subdir in clean_subdirs:
        result = subprocess.run(["python3", script_path, subdir], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(subdir))

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_subdirs)} clean modified/rejected: {', '.join(failed_clean)}"

def test_sanitizer_evil_corpus():
    script_path = "/home/user/sanitizer.py"
    evil_corpus_dir = "/app/corpus/evil"

    assert os.path.isdir(evil_corpus_dir), "Evil corpus directory missing."

    evil_subdirs = [os.path.join(evil_corpus_dir, d) for d in os.listdir(evil_corpus_dir) 
                    if os.path.isdir(os.path.join(evil_corpus_dir, d))]

    failed_evil = []
    for subdir in evil_subdirs:
        result = subprocess.run(["python3", script_path, subdir], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(subdir))

    assert not failed_evil, f"{len(failed_evil)} of {len(evil_subdirs)} evil bypassed: {', '.join(failed_evil)}"