# test_final_state.py

import os
import subprocess
import pytest

def test_rust_binary_compiled_and_works():
    binary_path = "/app/ws-route-parser/target/release/ws-route-parser"
    assert os.path.isfile(binary_path), f"Compiled Rust binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable"

    # Test the binary output
    result = subprocess.run(
        [binary_path, "/api/test?room=50"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Rust binary failed to execute"
    output = result.stdout.strip()
    assert "PATH=/api/test" in output, f"Unexpected PATH output from binary: {output}"
    assert "ROOM=50" in output, f"Unexpected ROOM output from binary: {output}"

def test_bash_script_exists_and_executable():
    script_path = "/home/user/ws_filter.sh"
    assert os.path.isfile(script_path), f"Bash script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Bash script at {script_path} is not executable"

def test_clean_corpus():
    script_path = "/home/user/ws_filter.sh"
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory not found at {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No files found in clean corpus"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, "r") as f:
            url = f.read().strip()

        result = subprocess.run(
            [script_path, url],
            capture_output=True,
            text=True
        )
        if result.returncode != 0 or "ALLOW" not in result.stdout:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}")

def test_evil_corpus():
    script_path = "/home/user/ws_filter.sh"
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory not found at {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No files found in evil corpus"

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, "r") as f:
            url = f.read().strip()

        result = subprocess.run(
            [script_path, url],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 or "DENY" not in result.stdout:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}")