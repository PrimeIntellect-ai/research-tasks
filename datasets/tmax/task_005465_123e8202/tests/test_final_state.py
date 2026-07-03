# test_final_state.py

import os
import subprocess
import pytest

def test_main_go_fixed():
    path = "/home/user/app/main.go"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "net/http/pprof" in content, "net/http/pprof is not imported in main.go"

    # Check if there is a read from jobChan
    assert "<-jobChan" in content.replace(" ", ""), "Background worker reading from jobChan is missing in main.go"

def test_load_test_exists():
    path = "/home/user/scripts/load_test.py"
    assert os.path.isfile(path), f"Python load test script {path} does not exist."

def test_heap_profile_exists():
    path = "/home/user/output_heap.pb.gz"
    assert os.path.isfile(path), f"Heap profile {path} does not exist."

    # Check if it's a valid gzip file
    with open(path, "rb") as f:
        magic_number = f.read(2)
    assert magic_number == b'\x1f\x8b', f"File {path} is not a valid gzip file."

def test_go_compiles():
    path = "/home/user/app/main.go"
    assert os.path.isfile(path), f"File {path} does not exist."

    result = subprocess.run(
        ["go", "build", "-o", "/dev/null", "main.go"],
        cwd="/home/user/app",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Go code failed to compile:\n{result.stderr}"