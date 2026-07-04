# test_final_state.py

import os
import re
import subprocess
import pytest

def test_leak_report_content():
    report_path = "/home/user/leak_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {report_path}, found {len(lines)}."

    assert lines[0] == "GHOST_ORPHAN_9921_DATA", f"Line 1 expected 'GHOST_ORPHAN_9921_DATA', got '{lines[0]}'."
    assert lines[1] == "1003", f"Line 2 expected '1003', got '{lines[1]}'."

def test_rust_code_fixed():
    main_rs_path = "/home/user/app/src/main.rs"
    assert os.path.isfile(main_rs_path), f"File {main_rs_path} does not exist."

    with open(main_rs_path, "r") as f:
        content = f.read()

    # Check that CACHE is cleaned up on timeout
    # A typical fix adds CACHE.lock().unwrap().remove(&id); inside `if timeout` or changes the return logic

    # We can verify that the cleanup occurs by checking if remove is called inside the timeout block 
    # or if the early return was removed so that the normal cleanup is reached.

    has_remove_in_timeout = re.search(r'if\s+timeout\s*\{[^}]*CACHE\.lock\(\)\.unwrap\(\)\.remove\(&id\);[^}]*\}', content)
    removed_early_return = not re.search(r'if\s+timeout\s*\{[^}]*return;[^}]*\}', content)
    used_drop_guard = "Drop" in content and "impl" in content

    assert has_remove_in_timeout or removed_early_return or used_drop_guard, \
        "The memory leak is not fixed. The request is not removed from CACHE when a timeout occurs."

def test_rust_project_compiles():
    app_dir = "/home/user/app"
    assert os.path.isdir(app_dir), f"Directory {app_dir} does not exist."

    result = subprocess.run(
        ["cargo", "check"],
        cwd=app_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"'cargo check' failed:\n{result.stderr}"