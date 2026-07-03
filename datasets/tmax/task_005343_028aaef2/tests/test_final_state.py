# test_final_state.py
import os
import subprocess
from pathlib import Path

def test_scripts_exist_and_executable():
    sanitizer_path = "/home/user/sanitizer.sh"
    bridge_path = "/home/user/run_bridge.sh"

    assert os.path.isfile(sanitizer_path), f"{sanitizer_path} does not exist or is not a file."
    assert os.access(sanitizer_path, os.X_OK), f"{sanitizer_path} is not executable."

    assert os.path.isfile(bridge_path), f"{bridge_path} does not exist or is not a file."
    assert os.access(bridge_path, os.X_OK), f"{bridge_path} is not executable."

def test_sanitizer_clean_corpus():
    clean_dir = Path("/app/corpora/clean")
    sanitizer_path = "/home/user/sanitizer.sh"

    assert clean_dir.exists() and clean_dir.is_dir(), "Clean corpus directory missing."

    modified_files = []

    for file_path in clean_dir.iterdir():
        if file_path.is_file():
            with open(file_path, "rb") as f:
                input_data = f.read()

            result = subprocess.run([sanitizer_path], input=input_data, capture_output=True)
            if result.stdout != input_data:
                modified_files.append(file_path.name)

    assert not modified_files, f"{len(modified_files)} of {len(list(clean_dir.iterdir()))} clean files modified: {', '.join(modified_files)}"

def test_sanitizer_evil_corpus():
    evil_dir = Path("/app/corpora/evil")
    sanitizer_path = "/home/user/sanitizer.sh"

    assert evil_dir.exists() and evil_dir.is_dir(), "Evil corpus directory missing."

    bypassed_files = []

    for file_path in evil_dir.iterdir():
        if file_path.is_file():
            with open(file_path, "rb") as f:
                input_data = f.read()

            result = subprocess.run([sanitizer_path], input=input_data, capture_output=True)
            if result.stdout.strip():
                bypassed_files.append(file_path.name)

    assert not bypassed_files, f"{len(bypassed_files)} of {len(list(evil_dir.iterdir()))} evil files bypassed: {', '.join(bypassed_files)}"

def test_bridge_script_content():
    bridge_path = "/home/user/run_bridge.sh"

    with open(bridge_path, "r") as f:
        content = f.read()

    assert "8081" in content, "run_bridge.sh does not reference port 8081"
    assert "8082" in content, "run_bridge.sh does not reference port 8082"
    assert "sanitizer.sh" in content, "run_bridge.sh does not reference sanitizer.sh"