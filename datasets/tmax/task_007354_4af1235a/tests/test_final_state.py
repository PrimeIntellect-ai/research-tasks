# test_final_state.py

import os
import pytest

def test_final_inventory_contents():
    """Test that final_inventory.txt contains the exact expected sorted output."""
    final_inventory_path = "/home/user/artifact_manager/final_inventory.txt"

    assert os.path.isfile(final_inventory_path), f"File {final_inventory_path} is missing."

    with open(final_inventory_path, "r", encoding="utf-8") as f:
        content = f.read().strip().splitlines()

    expected_content = [
        "[bundle_1.tar.gz] fileA.bin",
        "[bundle_1.tar.gz] fileB.bin",
        "[bundle_3.tar.gz] fileD.bin"
    ]

    assert content == expected_content, f"Contents of {final_inventory_path} do not match the expected output. Got: {content}"

def test_curated_files_extracted():
    """Test that the inner files were properly extracted to the curated directory."""
    curated_dir = "/home/user/artifact_manager/curated"

    expected_files = ["fileA.bin", "fileB.bin", "fileD.bin"]
    for file in expected_files:
        file_path = os.path.join(curated_dir, file)
        assert os.path.isfile(file_path), f"Extracted file {file_path} is missing."

def test_rust_source_locking_mechanism():
    """Test that the Rust source code uses a file locking mechanism."""
    main_rs_path = "/home/user/artifact_manager/curator/src/main.rs"

    assert os.path.isfile(main_rs_path), f"Rust source file {main_rs_path} is missing."

    with open(main_rs_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Check for common locking keywords in Rust
    locking_keywords = ["lock_exclusive", "flock", "lock", "fs4", "fd-lock", "try_lock_exclusive"]

    has_lock = any(keyword in source_code for keyword in locking_keywords)
    assert has_lock, f"Rust source code in {main_rs_path} does not appear to use a file locking mechanism."

def test_run_all_script_exists():
    """Test that the bash script run_all.sh exists."""
    script_path = "/home/user/artifact_manager/run_all.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} is missing."