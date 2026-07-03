# test_final_state.py

import os
import subprocess
import pytest

def test_resolution_file_exists():
    path = "/home/user/resolution.txt"
    assert os.path.isfile(path), f"File {path} does not exist"

def test_resolution_file_content():
    path = "/home/user/resolution.txt"
    with open(path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, f"Expected at least 2 lines in {path}, found {len(lines)}"

    line1 = lines[0].replace(" ", "")
    line2 = lines[1].replace(" ", "")

    expected_formulas = ["1.0/(x-y)", "1.0_f64/(x-y)", "1./(x-y)", "1.0/(x-y)"]
    assert any(formula in line1 for formula in expected_formulas), \
        f"Line 1 does not contain the correct reverse-engineered formula. Got: {lines[0]}"

    assert line2 == "0.2", f"Line 2 does not contain the correct computed output. Expected '0.2', got: '{lines[1]}'"

def test_c_dependency_removed():
    path = "/home/user/weight_service/src/main.rs"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    assert 'extern "C"' not in content, "The FFI 'extern \"C\"' block was not removed from main.rs"
    assert "libcalc.so" not in content, "References to the C library should be removed"

def test_cargo_build_succeeds():
    path = "/home/user/weight_service"
    assert os.path.isdir(path), f"Directory {path} does not exist"

    result = subprocess.run(
        ["cargo", "build", "--release"], 
        cwd=path, 
        capture_output=True, 
        text=True
    )

    assert result.returncode == 0, \
        f"cargo build --release failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"