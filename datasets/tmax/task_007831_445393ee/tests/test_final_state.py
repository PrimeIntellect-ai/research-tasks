# test_final_state.py

import os
import subprocess
import sys
import pytest

def test_venv_and_packages():
    """Verify the virtual environment exists and required packages are installed."""
    venv_python = "/home/user/venv/bin/python"
    assert os.path.isfile(venv_python), f"Virtual environment python not found at {venv_python}"

    cmd = [venv_python, "-c", "import pytest, hypothesis, responses, requests"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to import required packages in venv. Error: {result.stderr}"

def test_bytecode_txt():
    """Verify bytecode.txt exists and contains evidence of lock usage."""
    bytecode_path = "/home/user/bytecode.txt"
    assert os.path.isfile(bytecode_path), f"{bytecode_path} does not exist."

    with open(bytecode_path, "r") as f:
        content = f.read()

    assert "self" in content, "bytecode.txt does not contain 'self'"
    assert "lock" in content, "bytecode.txt does not contain 'lock'"

def test_test_sync_passes():
    """Verify test_sync.py exists and passes using the venv's pytest."""
    test_file = "/home/user/test_sync.py"
    assert os.path.isfile(test_file), f"{test_file} does not exist."

    venv_pytest = "/home/user/venv/bin/pytest"
    assert os.path.isfile(venv_pytest), f"pytest not found in venv at {venv_pytest}"

    cmd = [venv_pytest, test_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"test_sync.py failed to pass. Output:\n{result.stdout}\n{result.stderr}"

def test_sync_manager_logic():
    """Verify the logic of SyncManager programmatically using the venv python."""
    verify_script = "/home/user/verify_internal_test.py"
    script_content = """
import sys
from sync_manager import SyncManager
import requests
import responses

@responses.activate
def test_correct_logic():
    manager = SyncManager()
    manager.cache = {"a": 1}

    # Test Failure
    responses.add(responses.POST, "http://api.example.com/sync", status=500)
    try:
        manager.sync({"b": 2})
    except Exception:
        pass

    assert manager.cache == {"a": 1}, "Cache was modified despite API failure"

    # Test Success
    responses.add(responses.POST, "http://api.example.com/sync", status=200)
    manager.sync({"b": 2})

    # Accept either update or full replacement depending on interpretation, 
    # but the prompt says "incorporates the new data" usually meaning update.
    assert manager.cache == {"a": 1, "b": 2} or manager.cache == {"b": 2}, "Cache not updated properly on success"

if __name__ == "__main__":
    test_correct_logic()
"""
    with open(verify_script, "w") as f:
        f.write(script_content)

    venv_python = "/home/user/venv/bin/python"
    cmd = [venv_python, verify_script]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/home/user")

    # Clean up the script
    if os.path.exists(verify_script):
        os.remove(verify_script)

    assert result.returncode == 0, f"SyncManager logic verification failed. Output:\n{result.stderr}\n{result.stdout}"

def test_analyze_script_exists():
    """Verify analyze.py exists."""
    analyze_path = "/home/user/analyze.py"
    assert os.path.isfile(analyze_path), f"{analyze_path} does not exist."