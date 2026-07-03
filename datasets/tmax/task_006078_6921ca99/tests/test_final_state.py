# test_final_state.py
import os
import re

def test_cpp_source_fixed():
    path = "/home/user/pi_sim.cpp"
    assert os.path.isfile(path), f"File not found: {path}"
    with open(path, "r") as f:
        code = f.read()

    # Verify 'atomic' was removed
    assert "atomic" not in code, "The atomic pragma was not removed from pi_sim.cpp"

    # Verify 'reduction' was added
    assert "reduction" in code, "OpenMP reduction clause not found in pi_sim.cpp"
    assert "+:sum" in code.replace(" ", ""), "Reduction clause does not correctly specify +:sum"

def test_cpp_executable_exists():
    path = "/home/user/pi_sim"
    assert os.path.isfile(path), f"Executable not found: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_bash_script_exists():
    path = "/home/user/run_experiments.sh"
    assert os.path.isfile(path), f"Bash script not found: {path}"

def test_times_csv_created():
    path = "/home/user/times.csv"
    assert os.path.isfile(path), f"CSV file not found: {path}"
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) == 100, f"times.csv has {len(lines)} lines, expected exactly 100"
    for line in lines:
        try:
            float(line)
        except ValueError:
            assert False, f"Line in times.csv is not a valid float: '{line}'"

def test_python_script_exists():
    path = "/home/user/analyze.py"
    assert os.path.isfile(path), f"Python script not found: {path}"

def test_ci_txt_created():
    path = "/home/user/ci.txt"
    assert os.path.isfile(path), f"ci.txt not found: {path}"
    with open(path, "r") as f:
        content = f.read().strip()

    match = re.match(r'^\d+\.\d+,\d+\.\d+$', content)
    assert match, f"ci.txt format incorrect, expected 'float,float' but got: '{content}'"

def test_histogram_png_created():
    path = "/home/user/histogram.png"
    assert os.path.isfile(path), f"histogram.png not found: {path}"
    with open(path, "rb") as f:
        header = f.read(8)
    # Check PNG magic number
    assert header == b'\x89PNG\r\n\x1a\n', f"File is not a valid PNG image: {path}"