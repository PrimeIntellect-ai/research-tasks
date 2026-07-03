# test_final_state.py

import os
import subprocess
import shutil
import tempfile
import pytest

def test_crash_tx_file():
    path = "/home/user/crash_tx.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you create it?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert "TXN-8842" in content, f"Expected 'TXN-8842' in {path}, but found '{content}'"

def test_rust_fix_compiles_and_works():
    src_dir = "/home/user/parser"
    assert os.path.isdir(src_dir), f"Directory {src_dir} does not exist."

    # Copy the project to a temporary directory to avoid dirtying the student's workspace
    with tempfile.TemporaryDirectory() as tmpdir:
        test_project = os.path.join(tmpdir, "parser")
        shutil.copytree(src_dir, test_project)

        main_rs_path = os.path.join(test_project, "src", "main.rs")
        assert os.path.isfile(main_rs_path), "src/main.rs is missing from the parser project"

        # Append a test to verify the fix
        test_code = """
#[test]
fn test_oob_graceful_handling() {
    let bad_packet = vec![50, 50, 1, 2, 3]; // len 5, header_len 150
    let res = extract_payload(&bad_packet);
    assert_eq!(res.len(), 0, "Expected empty slice for out-of-bounds header_len");
}
"""
        with open(main_rs_path, "a") as f:
            f.write("\n" + test_code)

        # Run cargo test
        result = subprocess.run(
            ["cargo", "test"],
            cwd=test_project,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, (
            "The Rust project failed to compile or pass the out-of-bounds test.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}\n"
            "Ensure that extract_payload gracefully returns an empty slice when header_len > packet.len()."
        )