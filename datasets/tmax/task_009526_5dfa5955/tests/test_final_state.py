# test_final_state.py
import os
import json
import subprocess
import pytest

def test_virtual_environment_exists():
    """Test that the virtual environment is created at the correct location."""
    venv_dir = '/home/user/scienv'
    assert os.path.exists(venv_dir), f"Virtual environment directory {venv_dir} does not exist."
    assert os.path.isdir(venv_dir), f"{venv_dir} is not a directory."
    python_bin = os.path.join(venv_dir, 'bin', 'python')
    assert os.path.exists(python_bin), f"Python binary not found at {python_bin}."

def test_packages_installed_in_venv():
    """Test that mpi4py, numpy, and scipy are installed in the virtual environment."""
    venv_python = '/home/user/scienv/bin/python'
    if not os.path.exists(venv_python):
        pytest.skip("Virtual environment Python binary missing.")

    # Check if packages can be imported
    cmd = [venv_python, '-c', 'import mpi4py, numpy, scipy']
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to import required packages in venv. Error: {result.stderr}"

def test_mpi_script_exists():
    """Test that the MPI profiler script exists."""
    script_file = '/home/user/mpi_profiler.py'
    assert os.path.exists(script_file), f"MPI script {script_file} does not exist."
    assert os.path.isfile(script_file), f"{script_file} is not a file."

def test_profiling_report_exists():
    """Test that the profiling report JSON file exists."""
    report_file = '/home/user/profiling_report.json'
    assert os.path.exists(report_file), f"Profiling report {report_file} does not exist."
    assert os.path.isfile(report_file), f"{report_file} is not a file."

def test_profiling_report_contents():
    """Test that the profiling report contains the correct data."""
    report_file = '/home/user/profiling_report.json'
    if not os.path.exists(report_file):
        pytest.skip(f"{report_file} missing, skipping content test.")

    try:
        with open(report_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON from {report_file}: {e}")

    assert 'processes' in data, "Key 'processes' missing in JSON report."
    assert data['processes'] == 4, f"Expected 'processes' to be 4, got {data['processes']}."

    assert 'wasserstein_distance' in data, "Key 'wasserstein_distance' missing in JSON report."
    dist = data['wasserstein_distance']
    assert isinstance(dist, (int, float)), f"Expected 'wasserstein_distance' to be a float, got {type(dist)}."
    assert abs(dist - 0.05) < 1e-4, f"Expected 'wasserstein_distance' to be ~0.05, got {dist}."