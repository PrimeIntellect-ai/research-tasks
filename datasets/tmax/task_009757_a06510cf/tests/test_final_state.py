# test_final_state.py

import os
import subprocess

def test_concentrations_file_exists_and_correct():
    """Test that the output file exists and contains the correct computed concentrations."""
    filepath = "/home/user/concentrations.txt"
    assert os.path.isfile(filepath), f"Output file {filepath} does not exist. Did you run the cargo command and redirect output?"

    with open(filepath, "r") as f:
        content = f.read().strip()

    expected = "Component A: 2.07\nComponent B: 2.82"
    assert content == expected, f"Content of {filepath} is incorrect.\nExpected:\n{expected}\n\nGot:\n{content}"

def test_lib_rs_bug_fixed():
    """Test that the bug in lib.rs has been fixed."""
    lib_path = "/home/user/spectro_solve/src/lib.rs"
    assert os.path.isfile(lib_path), f"File {lib_path} does not exist."

    with open(lib_path, "r") as f:
        content = f.read()

    assert "m1 * b2 + b1 * m2" not in content, "The mathematical bug 'm1 * b2 + b1 * m2' is still present in src/lib.rs. It should use subtraction for Cramer's rule."

def test_cargo_test_passes():
    """Test that the Rust test suite now passes successfully."""
    project_dir = "/home/user/spectro_solve"
    assert os.path.isdir(project_dir), f"Directory {project_dir} does not exist."

    result = subprocess.run(
        ["cargo", "test"], 
        cwd=project_dir, 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, f"'cargo test' failed in {project_dir}. The bug might not be correctly fixed.\nStdout: {result.stdout}\nStderr: {result.stderr}"