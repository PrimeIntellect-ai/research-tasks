# test_final_state.py

import os
import tarfile
import tempfile
import pytest

def test_process_logs_rs_exists():
    path = "/home/user/process_logs.rs"
    assert os.path.isfile(path), f"Expected Rust source file at {path}"

def test_original_logs_exist():
    path = "/home/user/project_logs.txt"
    assert os.path.isfile(path), f"Original log file {path} should not be deleted."

def test_clean_logs_tarball():
    tar_path = "/home/user/clean_logs.tar.gz"
    assert os.path.isfile(tar_path), f"Tarball {tar_path} is missing."
    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar archive."

    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getnames()
        # Ensure part_1.txt through part_10.txt are in the tarball
        for i in range(1, 11):
            # The tarball might include the directory prefix, e.g., home/user/chunks/part_1.txt
            # Let's check if there's any member ending with part_{i}.txt
            found = any(m.endswith(f"part_{i}.txt") for m in members)
            assert found, f"Chunk part_{i}.txt is missing from the tarball."

        # Extract and verify contents
        with tempfile.TemporaryDirectory() as tmpdir:
            tar.extractall(path=tmpdir)

            # Find the actual extracted files
            extracted_files = []
            for root, _, files in os.walk(tmpdir):
                for f in files:
                    if f.startswith("part_") and f.endswith(".txt"):
                        extracted_files.append(os.path.join(root, f))

            assert len(extracted_files) == 10, f"Expected 10 chunk files, found {len(extracted_files)}"

            for fpath in extracted_files:
                with open(fpath, "r") as f:
                    lines = f.readlines()
                assert len(lines) == 50, f"File {fpath} does not have exactly 50 lines."

                content = "".join(lines)
                assert "API_KEY=xyz123" not in content, f"Unsanitized API_KEY=xyz123 found in {fpath}"
                assert "API_KEY=abc999" not in content, f"Unsanitized API_KEY=abc999 found in {fpath}"

                fname = os.path.basename(fpath)
                if fname == "part_1.txt":
                    assert "API_KEY=REDACTED" in lines[44], f"Expected REDACTED API key on line 45 of part_1.txt"
                elif fname == "part_3.txt":
                    assert "API_KEY=REDACTED" in lines[19], f"Expected REDACTED API key on line 20 of part_3.txt"

def test_symlinks():
    symlinks_dir = "/home/user/symlinks"
    assert os.path.isdir(symlinks_dir), f"Directory {symlinks_dir} is missing."

    for i in range(2, 11, 2):
        symlink_path = os.path.join(symlinks_dir, f"active_{i}.txt")
        assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

        target = os.readlink(symlink_path)
        expected_target = f"../chunks/part_{i}.txt"
        assert target == expected_target, f"Symlink {symlink_path} points to {target}, expected {expected_target}"

def test_chunks_directory_exists():
    chunks_dir = "/home/user/chunks"
    assert os.path.isdir(chunks_dir), f"Directory {chunks_dir} is missing."
    for i in range(1, 11):
        chunk_path = os.path.join(chunks_dir, f"part_{i}.txt")
        assert os.path.isfile(chunk_path), f"Chunk file {chunk_path} is missing."