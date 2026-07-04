# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_reproduce_sh_exists_and_executable():
    path = "/home/user/reproduce.sh"
    assert os.path.isfile(path), f"File {path} does not exist"

    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"File {path} is not executable"

    with open(path, "r") as f:
        content = f.read()
        assert "go test" in content, f"File {path} does not appear to run 'go test'"

def test_fix_patch_exists_and_valid():
    path = "/home/user/fix.patch"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        content = f.read()
        assert "---" in content and "+++" in content, f"File {path} does not look like a valid unified diff/patch file"

def test_sensor_go_fixed():
    path = "/home/user/sensor/sensor.go"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        content = f.read()
        assert "[]float64" in content, "Payload Readings should be changed to float64 to fix precision issues"
        assert "base64.URLEncoding" in content, "Should use base64.URLEncoding to fix the parsing issue"

def test_go_test_passes_consistently():
    # Run go test multiple times to ensure the intermittent failures are fixed
    for i in range(10):
        result = subprocess.run(
            ["go", "test"], 
            cwd="/home/user/sensor", 
            capture_output=True, 
            text=True
        )
        assert result.returncode == 0, f"go test failed on run {i+1}. Output:\n{result.stdout}\n{result.stderr}"