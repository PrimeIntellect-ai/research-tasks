# test_final_state.py
import os
import subprocess
import hashlib
import pytest

PIPELINE_DIR = '/home/user/ml_pipeline'
VENV_PYTHON = '/home/user/venv/bin/python'
PROCESS_SCRIPT = os.path.join(PIPELINE_DIR, 'process_data.py')
RUN_SCRIPT = os.path.join(PIPELINE_DIR, 'run.sh')
PLOT_FILE = os.path.join(PIPELINE_DIR, 'pca_plot.png')
SUMMARY_FILE = os.path.join(PIPELINE_DIR, 'summary.tsv')

def get_file_hash(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def test_packages_installed():
    """Verify required packages are installed in the virtual environment."""
    assert os.path.exists(VENV_PYTHON), "Virtual environment python not found."
    result = subprocess.run([VENV_PYTHON, '-c', 'import numpy, scipy, sklearn, matplotlib'], capture_output=True)
    assert result.returncode == 0, "Not all required packages are installed in the virtual environment."

def test_process_data_modifications():
    """Verify process_data.py was modified correctly."""
    with open(PROCESS_SCRIPT, 'r') as f:
        content = f.read()

    assert 'plt.show()' not in content, "plt.show() should be removed from process_data.py"
    assert 'pca_plot.png' in content, "process_data.py should save the plot to pca_plot.png"
    assert 'sys.argv' in content, "process_data.py should read the seed from command line arguments"

def test_run_sh_execution_and_reproducibility():
    """Run run.sh, verify outputs, reproducibility, and TSV formatting."""
    # Clean up any existing outputs from user's manual testing
    if os.path.exists(PLOT_FILE):
        os.remove(PLOT_FILE)
    if os.path.exists(SUMMARY_FILE):
        os.remove(SUMMARY_FILE)

    # Run with seed 42
    result1 = subprocess.run(['bash', RUN_SCRIPT, '42'], cwd=PIPELINE_DIR, capture_output=True, text=True)
    assert result1.returncode == 0, f"run.sh failed with seed 42. stderr: {result1.stderr}"

    assert os.path.exists(PLOT_FILE), "pca_plot.png was not generated."
    hash_42_1 = get_file_hash(PLOT_FILE)

    assert os.path.exists(SUMMARY_FILE), "summary.tsv was not generated."
    with open(SUMMARY_FILE, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 2, "summary.tsv should have a header and one data row after one run."
    assert lines[0] == "Seed\tP-Value\tCI_Lower\tCI_Upper", "summary.tsv header is incorrect."
    assert lines[1].startswith("42\t"), "summary.tsv data row should start with the seed."

    # Run again with seed 42
    os.remove(PLOT_FILE)
    result2 = subprocess.run(['bash', RUN_SCRIPT, '42'], cwd=PIPELINE_DIR, capture_output=True, text=True)
    assert result2.returncode == 0, "run.sh failed on second run."

    hash_42_2 = get_file_hash(PLOT_FILE)
    assert hash_42_1 == hash_42_2, "pca_plot.png is not reproducible for the same seed."

    with open(SUMMARY_FILE, 'r') as f:
        lines = f.read().strip().split('\n')
    assert len(lines) == 3, "summary.tsv should have 3 lines after two runs."
    assert lines[1] == lines[2], "Subsequent runs with the same seed should append identical rows."

    # Run with seed 99
    os.remove(PLOT_FILE)
    result3 = subprocess.run(['bash', RUN_SCRIPT, '99'], cwd=PIPELINE_DIR, capture_output=True, text=True)
    assert result3.returncode == 0, "run.sh failed with seed 99."

    hash_99 = get_file_hash(PLOT_FILE)
    assert hash_99 != hash_42_1, "pca_plot.png should change when a different seed is used."

    with open(SUMMARY_FILE, 'r') as f:
        lines = f.read().strip().split('\n')
    assert len(lines) == 4, "summary.tsv should have 4 lines after three runs."
    assert lines[3].startswith("99\t"), "summary.tsv data row should start with the new seed."

def test_run_sh_default_seed():
    """Verify run.sh uses default seed 42 when no argument is provided."""
    if os.path.exists(PLOT_FILE):
        os.remove(PLOT_FILE)

    result = subprocess.run(['bash', RUN_SCRIPT], cwd=PIPELINE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, "run.sh failed when no arguments were provided."

    with open(SUMMARY_FILE, 'r') as f:
        lines = f.read().strip().split('\n')

    last_line = lines[-1]
    assert last_line.startswith("42\t"), "run.sh should default to seed 42 if no argument is provided."