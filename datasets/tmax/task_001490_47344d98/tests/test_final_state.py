# test_final_state.py
import os

def test_executable_exists():
    executable_path = "/home/user/mcmc_opt"
    assert os.path.isfile(executable_path), f"Compiled executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable"

def test_output_file_and_value():
    output_path = "/home/user/output.txt"
    assert os.path.isfile(output_path), f"Output file not found at {output_path}"

    with open(output_path, "r") as f:
        content = f.read().strip()

    try:
        z_value = float(content)
    except ValueError:
        raise AssertionError(f"Output file {output_path} does not contain a valid float. Found: '{content}'")

    expected_z = 6.25
    tolerance = 0.1
    assert abs(z_value - expected_z) <= tolerance, f"Expected z value near {expected_z}, but got {z_value}"

def test_cpp_bottleneck_fixed():
    cpp_file = "/home/user/mcmc_opt.cpp"
    assert os.path.isfile(cpp_file), f"C++ source file missing: {cpp_file}"

    with open(cpp_file, "r") as f:
        content = f.read()

    # The original bottleneck was calling load_data() inside log_likelihood.
    # We check that the exact inefficient line is removed or modified.
    inefficient_line = "vector<double> y = load_data();"

    # A robust check is to ensure that load_data is not called inside the log_likelihood function body.
    # For simplicity, we can just assert the exact old bottleneck line is gone.
    assert inefficient_line not in content, "The deliberate bottleneck (calling load_data() inside the loop) is still present in the C++ file."