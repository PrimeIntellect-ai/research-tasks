# test_final_state.py

import os
import subprocess
import re

def test_results_file_exists_and_passed():
    results_path = "/home/user/test_results.txt"
    assert os.path.exists(results_path), f"File {results_path} does not exist."
    with open(results_path, "r") as f:
        content = f.read()
    assert "3 passed" in content, "Test results do not indicate that 3 tests passed. Make sure to run pytest and save the output to test_results.txt."

def test_rust_code_fixed():
    lib_path = "/home/user/expr-eval/src/lib.rs"
    assert os.path.exists(lib_path), f"File {lib_path} does not exist."
    with open(lib_path, "r") as f:
        content = f.read()

    # Check for logical fixes in subtraction and division
    assert re.search(r'"-"\s*=>\s*a\s*-\s*b', content), "Subtraction bug in lib.rs not fixed. Expected 'a - b'."
    assert re.search(r'"/"\s*=>\s*a\s*/\s*b', content), "Division bug in lib.rs not fixed. Expected 'a / b'."

def test_rust_compiles():
    project_dir = "/home/user/expr-eval"
    assert os.path.isdir(project_dir), f"Directory {project_dir} does not exist."

    result = subprocess.run(
        ["cargo", "check"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Rust code failed to compile (cargo check returned non-zero).\nStderr:\n{result.stderr}"