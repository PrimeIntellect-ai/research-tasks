# test_final_state.py
import os
import stat
import pytest

def test_extract_executable_exists():
    path = "/home/user/extract"
    assert os.path.isfile(path), f"Executable {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_features_txt_exists_and_correct():
    path = "/home/user/features.txt"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip().split("\n")

    assert len(content) == 10, f"Expected 10 lines in {path}, got {len(content)}."

    # Check for NaNs
    for line in content:
        parts = line.split()
        assert len(parts) == 2, f"Expected 2 columns in line: '{line}'"
        assert parts[1].lower() != "nan", f"Found NaN in {path}, the bug was not fixed correctly."

    # Isolated nodes 8 and 9 should have mean neighbor degree 0
    node_8 = [line for line in content if line.startswith("8 ")]
    node_9 = [line for line in content if line.startswith("9 ")]

    assert node_8, "Node 8 missing from features.txt"
    assert node_9, "Node 9 missing from features.txt"

    assert float(node_8[0].split()[1]) == 0.0, "Node 8 should have mean neighbor degree 0."
    assert float(node_9[0].split()[1]) == 0.0, "Node 9 should have mean neighbor degree 0."

def test_density_sh_exists():
    path = "/home/user/density.sh"
    assert os.path.isfile(path), f"Script {path} is missing."
    # It should be executable, but we can just check if it exists and has content
    st = os.stat(path)
    assert st.st_size > 0, f"Script {path} is empty."

def test_density_log_correct():
    path = "/home/user/density.log"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()

    expected = "Bin 0: 2\nBin 1: 4\nBin 2: 4\nBin 3: 0"
    assert content == expected, f"Content of {path} does not match expected output.\nExpected:\n{expected}\nActual:\n{content}"