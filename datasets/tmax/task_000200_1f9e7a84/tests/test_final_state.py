# test_final_state.py

import os
import stat
import subprocess

def test_fixed_service_exists_and_executable():
    path = "/home/user/fixed_service.sh"
    assert os.path.exists(path), f"Missing fixed service script: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script is not executable: {path}"

def test_final_variance_correct():
    path = "/home/user/final_variance.txt"
    assert os.path.exists(path), f"Missing final variance file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"Content of {path} is not a valid number: {content}"

    assert abs(val - 8.25) < 1e-5, f"Expected final variance to be 8.25, got {val}"

def test_fixed_service_logic():
    path = "/home/user/fixed_service.sh"
    with open(path, "r") as f:
        content = f.read()

    # Check that it doesn't just infinitely append to a bash array like the original
    # If it uses bash arrays, it should have a way to remove old elements or use modulo
    if "history+=(" in content or "history+=(" in content.replace(" ", ""):
        assert "unset" in content or "shift" in content or "${history[@]:" in content, \
            "Script still appears to append to an array without removing old elements (memory leak)."