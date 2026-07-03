# test_final_state.py

import os
import re
import stat

def test_cpp_file_exists():
    """Check that the C++ source file exists."""
    file_path = "/home/user/analyze_mutations.cpp"
    assert os.path.isfile(file_path), f"C++ program {file_path} is missing."

def test_pipeline_script_exists_and_executable():
    """Check that pipeline.sh exists and is executable."""
    file_path = "/home/user/pipeline.sh"
    assert os.path.isfile(file_path), f"Bash script {file_path} is missing."

    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script {file_path} is not executable."

def test_mcmc_samples_output():
    """Check that mcmc_samples.csv is created and has exactly 10000 samples."""
    file_path = "/home/user/mcmc_samples.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) == 10000, f"Expected exactly 10000 lines in {file_path}, but found {len(lines)}."

    # Check that all lines are valid floats
    for i, line in enumerate(lines):
        try:
            float(line.strip())
        except ValueError:
            assert False, f"Line {i+1} in {file_path} is not a valid float: '{line}'"

def test_results_output():
    """Check that results.txt exists, has the correct format, and the value is within bounds."""
    file_path = "/home/user/results.txt"
    assert os.path.isfile(file_path), f"Results file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read()

    match = re.search(r"Mean_Posterior:\s*([0-9]*\.?[0-9]+)", content)
    assert match is not None, f"Could not find 'Mean_Posterior: <value>' in {file_path}. File content:\n{content}"

    mean_val = float(match.group(1))
    assert 0.08 < mean_val < 0.15, f"Mean posterior value {mean_val} is out of the expected bounds (0.08, 0.15)."