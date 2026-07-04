# test_final_state.py
import os
import subprocess
import numpy as np
import pytest

def test_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    executable = "/app/c_port/ste_processor"
    assert os.path.isfile(executable), f"Executable {executable} not found. Did the Makefile run successfully?"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_mae_metric():
    """Run both the Python reference and the C program, and compare their outputs using MAE."""
    executable = "/app/c_port/ste_processor"
    py_script = "/app/processor.py"
    wav_file = "/app/recording.wav"

    py_out = "/tmp/py_out.txt"
    c_out = "/tmp/c_out.txt"

    # Run Python reference
    py_cmd = ["python3", py_script, wav_file, py_out]
    result_py = subprocess.run(py_cmd, capture_output=True, text=True)
    assert result_py.returncode == 0, f"Python script failed to run: {result_py.stderr}"

    # Run C program
    c_cmd = [executable, wav_file, c_out]
    result_c = subprocess.run(c_cmd, capture_output=True, text=True)
    assert result_c.returncode == 0, f"C program failed to run: {result_c.stderr}"

    # Ensure outputs were generated
    assert os.path.isfile(py_out), "Python output file was not generated."
    assert os.path.isfile(c_out), "C output file was not generated."

    # Read outputs
    with open(py_out, 'r') as f:
        ref = np.array([float(line.strip()) for line in f if line.strip()])
    with open(c_out, 'r') as f:
        test = np.array([float(line.strip()) for line in f if line.strip()])

    # Check lengths
    assert len(ref) == len(test), f"Length mismatch between outputs: Python={len(ref)}, C={len(test)}"

    # Compute MAE
    mae = np.mean(np.abs(ref - test))
    threshold = 0.001

    assert mae <= threshold, f"MAE {mae:.6f} exceeds the allowed threshold of {threshold}. The C logic does not match the Python reference closely enough."