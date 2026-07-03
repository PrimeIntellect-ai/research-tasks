# test_final_state.py

import os
import subprocess
import pytest

def test_error_count_file():
    error_count_path = "/home/user/error_count.txt"
    assert os.path.isfile(error_count_path), f"File {error_count_path} does not exist."

    with open(error_count_path, "r") as f:
        content = f.read().strip()

    assert content == "4", f"Expected error count to be '4', but got '{content}'."

def test_cargo_test_passes():
    project_dir = "/home/user/log-tracer"
    assert os.path.isdir(project_dir), f"Directory {project_dir} does not exist."

    result = subprocess.run(
        ["cargo", "test"],
        cwd=project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_circular_trace_exists():
    main_rs_path = "/home/user/log-tracer/src/main.rs"
    assert os.path.isfile(main_rs_path), f"File {main_rs_path} does not exist."

    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "test_circular_trace" in content, "The regression test 'test_circular_trace' was not found in main.rs."
    assert "#[test]" in content, "No #[test] attribute found in main.rs."

def test_fix_implemented():
    main_rs_path = "/home/user/log-tracer/src/main.rs"
    with open(main_rs_path, "r") as f:
        content = f.read()

    # Check for some form of visited tracking
    has_hashset = "HashSet" in content
    has_btreeset = "BTreeSet" in content
    has_visited = "visited" in content.lower()
    has_canonicalize = "canonicalize" in content

    assert any([has_hashset, has_btreeset, has_visited, has_canonicalize]), \
        "Could not find evidence of a visited files tracking mechanism (e.g., HashSet, canonicalize, or 'visited' variable) in main.rs."