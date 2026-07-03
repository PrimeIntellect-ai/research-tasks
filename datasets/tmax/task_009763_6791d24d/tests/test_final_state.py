# test_final_state.py

import os
import pytest

def test_slip_attempts_log():
    log_path = "/home/user/slip_attempts.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_malicious_paths = {
        "../../../../../home/user/hacked.txt",
        "/etc/passwd",
        "absolute_trick/../../../../../../tmp/pwn"
    }

    actual_paths = set(lines)
    assert actual_paths == expected_malicious_paths, f"slip_attempts.log does not contain the exact expected malicious paths. Expected {expected_malicious_paths}, got {actual_paths}"
    assert len(lines) == 3, f"slip_attempts.log should contain exactly 3 lines, but found {len(lines)}"

def test_safe_files_extracted():
    expected_files = {
        "/home/user/extracted/safe_file.txt": "This is safe data.",
        "/home/user/extracted/nested/dir/safe2.txt": "More safe data.",
        "/home/user/extracted/safe3.txt": "Sneaky but technically safe if resolved strictly."
    }

    for path, expected_content in expected_files.items():
        assert os.path.isfile(path), f"Safe file missing: {path}"
        with open(path, "r") as f:
            content = f.read()
        assert content == expected_content, f"Content mismatch in {path}. Expected '{expected_content}', got '{content}'"

def test_malicious_files_not_extracted():
    malicious_paths = [
        "/home/user/hacked.txt",
        "/tmp/pwn"
    ]

    for path in malicious_paths:
        assert not os.path.exists(path), f"Malicious file was extracted outside the target directory: {path}"

def test_rust_project_exists():
    project_dir = "/home/user/wal_extractor"
    assert os.path.isdir(project_dir), f"Rust project directory missing: {project_dir}"

    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml missing in {project_dir}"

    src_dir = os.path.join(project_dir, "src")
    assert os.path.isdir(src_dir), f"src directory missing in {project_dir}"

    main_rs = os.path.join(src_dir, "main.rs")
    assert os.path.isfile(main_rs), f"main.rs missing in {src_dir}"