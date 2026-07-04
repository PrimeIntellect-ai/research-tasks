# test_final_state.py

import os
import pytest

def test_resolve_py_exists_and_imports_asyncio():
    script_path = "/home/user/resolve.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "import asyncio" in content or "from asyncio" in content, "The script does not seem to import asyncio."
    assert "asyncio.Queue" in content or "Queue" in content, "The script does not seem to use asyncio.Queue."

def test_link_results_log_content():
    log_path = "/home/user/link_results.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    expected_lines = [
        "AppCore: SUCCESS",
        "AppData: FAILED",
        "AppNet: FAILED",
        "AppUI: SUCCESS",
        "AppUtil: SUCCESS"
    ]

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"Content of {log_path} does not match expected output. Got: {lines}"