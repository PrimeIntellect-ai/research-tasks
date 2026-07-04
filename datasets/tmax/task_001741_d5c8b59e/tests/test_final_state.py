# test_final_state.py

import os
import glob
import subprocess
import pytest
import numpy as np

def test_spectro_tools_installed_and_fixed():
    """Verify that the package is installed and the NameError bug is fixed."""
    try:
        import spectro_tools.baseline
    except ImportError as e:
        pytest.fail(f"spectro_tools is not installed properly or cannot be imported: {e}")

    # Create a dummy signal to test if remove_baseline works without NameError
    intensity = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    try:
        corrected = spectro_tools.baseline.remove_baseline(intensity)
        assert isinstance(corrected, np.ndarray), "remove_baseline should return a numpy array."
    except NameError as e:
        pytest.fail(f"The bug in spectro_tools.baseline was not fixed (NameError encountered): {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred when calling remove_baseline: {e}")

def run_script_and_parse_log(input_dir):
    """Helper to run the agent's script and parse the output log."""
    script_path = "/home/user/sanitize_data.py"
    log_path = "/home/user/classification.log"

    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    # Remove log file if it exists to ensure we only read the current run's output
    if os.path.exists(log_path):
        os.remove(log_path)

    result = subprocess.run(
        ["python", script_path, "--input-dir", input_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert os.path.exists(log_path), f"Log file {log_path} was not created by the script."

    classifications = {}
    with open(log_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ": " in line:
                fname, status = line.split(": ", 1)
                classifications[fname] = status

    return classifications

def test_clean_corpus_accepted():
    """Verify that all clean signals are ACCEPTED."""
    clean_dir = "/app/data/clean/"
    assert os.path.isdir(clean_dir), f"Clean data directory {clean_dir} is missing."

    csv_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    assert len(csv_files) > 0, f"No CSV files found in {clean_dir}."

    classifications = run_script_and_parse_log(clean_dir)

    rejected = []
    missing = []

    for file_path in csv_files:
        fname = os.path.basename(file_path)
        if fname not in classifications:
            missing.append(fname)
        elif classifications[fname] != "ACCEPT":
            rejected.append(fname)

    errors = []
    if rejected:
        errors.append(f"{len(rejected)} of {len(csv_files)} clean modified (rejected): {', '.join(rejected[:5])}")
    if missing:
        errors.append(f"{len(missing)} files missing from log: {', '.join(missing[:5])}")

    if errors:
        pytest.fail("; ".join(errors))

def test_evil_corpus_rejected():
    """Verify that all evil signals are REJECTED."""
    evil_dir = "/app/data/evil/"
    assert os.path.isdir(evil_dir), f"Evil data directory {evil_dir} is missing."

    csv_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    assert len(csv_files) > 0, f"No CSV files found in {evil_dir}."

    classifications = run_script_and_parse_log(evil_dir)

    accepted = []
    missing = []

    for file_path in csv_files:
        fname = os.path.basename(file_path)
        if fname not in classifications:
            missing.append(fname)
        elif classifications[fname] != "REJECT":
            accepted.append(fname)

    errors = []
    if accepted:
        errors.append(f"{len(accepted)} of {len(csv_files)} evil bypassed (accepted): {', '.join(accepted[:5])}")
    if missing:
        errors.append(f"{len(missing)} files missing from log: {', '.join(missing[:5])}")

    if errors:
        pytest.fail("; ".join(errors))