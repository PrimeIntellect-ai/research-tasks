# test_final_state.py

import subprocess
import os
import glob
import sys
import pytest

def run_script(directory):
    script_path = "/home/user/manifest_filter.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    result = subprocess.run([sys.executable, script_path, directory], capture_output=True, text=True)
    return result.stdout.strip().split('\n'), result.stderr, result.returncode

def test_clean_corpus():
    clean_dir = "/home/user/data/clean_manifests/"
    files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert len(files) > 0, "No clean manifests found in the setup."

    stdout_lines, stderr, returncode = run_script(clean_dir)

    results = {}
    for line in stdout_lines:
        if ":" in line:
            filename, status = line.split(":", 1)
            results[filename.strip()] = status.strip()

    failed_files = []
    for f in files:
        basename = os.path.basename(f)
        if results.get(basename) != "ACCEPT":
            failed_files.append(basename)

    assert not failed_files, f"{len(failed_files)} of {len(files)} clean modified (rejected or missing): {failed_files}. Script stderr: {stderr}"

def test_evil_corpus():
    evil_dir = "/home/user/data/evil_manifests/"
    files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert len(files) > 0, "No evil manifests found in the setup."

    stdout_lines, stderr, returncode = run_script(evil_dir)

    results = {}
    for line in stdout_lines:
        if ":" in line:
            filename, status = line.split(":", 1)
            results[filename.strip()] = status.strip()

    failed_files = []
    for f in files:
        basename = os.path.basename(f)
        if results.get(basename) != "REJECT":
            failed_files.append(basename)

    assert not failed_files, f"{len(failed_files)} of {len(files)} evil bypassed (accepted or missing): {failed_files}. Script stderr: {stderr}"

def test_vendored_package_fixed():
    """Ensure the vendored package can be imported without errors."""
    lib_path = "/app/graph-backup-lib"
    assert os.path.isdir(lib_path), f"Directory {lib_path} is missing."

    # Try importing it in a subprocess to avoid polluting the test environment
    result = subprocess.run(
        [sys.executable, "-c", "import sys; sys.path.insert(0, '/app/graph-backup-lib'); import graph_backup_lib"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to import graph_backup_lib. The package is still broken.\nStderr: {result.stderr}"