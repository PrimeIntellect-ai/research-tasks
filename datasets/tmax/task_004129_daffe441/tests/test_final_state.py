# test_final_state.py

import os
import subprocess
import sys
import pytest

def test_vendored_package_installed_and_fixed():
    # Check if package is installed and importable
    try:
        import sql_graph_proj.compiler
    except ImportError:
        pytest.fail("The package 'sql-graph-proj' is not installed or importable.")

    # Check if compiler.py is fixed
    compiler_path = "/app/sql-graph-proj-1.0.0/sql_graph_proj/compiler.py"
    assert os.path.isfile(compiler_path), f"Compiler file missing: {compiler_path}"

    with open(compiler_path, "r") as f:
        content = f.read()

    assert " INNER JOIN " in content, "The ' CROSS JOIN ' bug was not fixed to ' INNER JOIN ' in compiler.py."
    assert " CROSS JOIN " not in content, "The ' CROSS JOIN ' bug is still present in compiler.py."

def test_setup_py_fixed():
    setup_path = "/app/sql-graph-proj-1.0.0/setup.py"
    assert os.path.isfile(setup_path), f"Setup file missing: {setup_path}"

    with open(setup_path, "r") as f:
        content = f.read()

    assert "sqlite3>=4.0" not in content, "The invalid 'sqlite3>=4.0' dependency is still in setup.py."

def test_adversarial_sql_filter():
    filter_script = "/home/user/sql_filter.py"
    assert os.path.isfile(filter_script), f"Filter script missing: {filter_script}"

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.sql')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.sql')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run([sys.executable, filter_script, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run([sys.executable, filter_script, ef], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))