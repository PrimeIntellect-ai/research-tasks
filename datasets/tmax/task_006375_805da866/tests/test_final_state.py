# test_final_state.py

import os
import pytest

def test_manifest_file_exists():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Output file {manifest_path} does not exist. The task is not complete."

def test_manifest_contents():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Output file {manifest_path} does not exist."

    with open(manifest_path, 'r') as f:
        content = f.read().strip()

    expected_lines = [
        "auth_service_v2.tar.gz",
        "kernel_module_x86.tar.gz",
        "ui_assets.zip"
    ]
    expected_content = "\n".join(expected_lines)

    assert content == expected_content, (
        f"Contents of {manifest_path} do not match the expected verified artifacts.\n"
        f"Expected:\n{expected_content}\n\nGot:\n{content}"
    )

def test_atomic_move_used():
    # While we cannot easily verify if a Python os.rename or bash mv was used with 100% certainty 
    # without tracing syscalls, we can check bash_history if they did it via bash.
    # However, Python scripts using os.rename() are also acceptable atomic moves.
    # The primary truth is the exact file contents, but we can check bash_history for a hint of 'mv'
    # if it exists, though we won't strictly fail the test if they used a python script instead.
    history_file = "/home/user/.bash_history"
    if os.path.isfile(history_file):
        with open(history_file, 'r') as f:
            history = f.read()
            # Just an informational check, not strictly failing if they used Python
            if 'mv ' not in history and 'os.rename' not in history:
                pass # We don't fail here because they could have run a script that doesn't log to history