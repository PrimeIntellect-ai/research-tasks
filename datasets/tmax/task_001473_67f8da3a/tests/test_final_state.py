# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/poly-parser"

def test_build_rs_configured():
    build_rs_path = os.path.join(PROJECT_DIR, "build.rs")
    assert os.path.isfile(build_rs_path), f"build.rs is missing at {build_rs_path}."
    with open(build_rs_path, "r") as f:
        content = f.read()

    assert "cc::Build" in content or "cc::" in content, "build.rs does not seem to use the 'cc' crate to build the C code."
    assert "fast_parse.c" in content, "build.rs does not reference 'fast_parse.c'."

def test_lib_rs_bug_fixed():
    lib_rs_path = os.path.join(PROJECT_DIR, "src", "lib.rs")
    assert os.path.isfile(lib_rs_path), f"lib.rs is missing at {lib_rs_path}."
    with open(lib_rs_path, "r") as f:
        content = f.read()

    assert "capacity()" not in content, "The bug using 'capacity()' is still present in lib.rs."
    assert "len()" in content, "The fix using 'len()' was not found in lib.rs."

def test_ci_workflow_created():
    ci_yml_path = os.path.join(PROJECT_DIR, ".github", "workflows", "ci.yml")
    assert os.path.isfile(ci_yml_path), f"CI workflow file is missing at {ci_yml_path}."

    with open(ci_yml_path, "r") as f:
        content = f.read()

    assert "ubuntu-latest" in content, "The CI workflow does not specify 'ubuntu-latest'."
    assert "cargo test" in content, "The CI workflow does not run 'cargo test'."

def test_review_completed_file():
    review_file = "/home/user/review_completed.txt"
    assert os.path.isfile(review_file), f"Review completed file is missing at {review_file}."

    with open(review_file, "r") as f:
        content = f.read().strip()

    assert content == "PR fixed and tested", f"Review completed file content is incorrect. Expected 'PR fixed and tested', got '{content}'."

def test_cargo_test_passes():
    try:
        result = subprocess.run(
            ["cargo", "test"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"'cargo test' failed. Output:\n{e.stdout}\n{e.stderr}")