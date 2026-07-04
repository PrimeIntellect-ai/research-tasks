# test_final_state.py
import os
import re
import subprocess
import pytest

CPP_FILE = "/home/user/analyze_spectra.cpp"
RESULT_FILE = "/home/user/svd_result.txt"
TEST_BIN = "/tmp/analyze_spectra_test"

def test_atomic_pragma_removed():
    assert os.path.exists(CPP_FILE), f"{CPP_FILE} does not exist."
    with open(CPP_FILE, 'r') as f:
        content = f.read()

    assert "#pragma omp atomic" not in content, "The atomic pragma was not removed from the C++ file."

def test_svd_result_format():
    assert os.path.exists(RESULT_FILE), f"{RESULT_FILE} does not exist."
    with open(RESULT_FILE, 'r') as f:
        content = f.read().strip()

    # Check if it's a number with exactly 5 decimal places
    match = re.match(r"^\d+\.\d{5}$", content)
    assert match is not None, f"File {RESULT_FILE} must contain only a numeric value formatted to exactly 5 decimal places. Found: '{content}'"

def test_determinism_and_correctness():
    assert os.path.exists(CPP_FILE), f"{CPP_FILE} does not exist."
    assert os.path.exists(RESULT_FILE), f"{RESULT_FILE} does not exist."

    with open(RESULT_FILE, 'r') as f:
        reported_val = f.read().strip()

    # Compile the student's C++ code
    compile_cmd = [
        "g++", "-O3", "-fopenmp", 
        "-I/usr/include/eigen3", "-I/usr/include/hdf5/serial", 
        CPP_FILE, 
        "-L/usr/lib/x86_64-linux-gnu/hdf5/serial", "-lhdf5", 
        "-o", TEST_BIN
    ]

    compilation = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compilation.returncode == 0, f"Compilation failed:\n{compilation.stderr}"

    # Run the binary multiple times to verify determinism
    outputs = []
    for _ in range(3):
        run_res = subprocess.run([TEST_BIN], capture_output=True, text=True)
        assert run_res.returncode == 0, f"Program execution failed:\n{run_res.stderr}"

        # Extract the singular value from the output
        # Expected output format: "Leading Singular Value: 123.45678"
        output_str = run_res.stdout.strip()
        match = re.search(r"Leading Singular Value:\s*(\d+\.\d+)", output_str)
        assert match is not None, f"Could not parse the singular value from program output:\n{output_str}"

        outputs.append(match.group(1))

    # Check determinism
    first_output = outputs[0]
    for out in outputs[1:]:
        assert out == first_output, "Program is still non-deterministic. Multiple runs produced different results."

    # Check correctness against the reported file
    assert reported_val == first_output, f"The value in {RESULT_FILE} ({reported_val}) does not match the deterministic output of the program ({first_output})."