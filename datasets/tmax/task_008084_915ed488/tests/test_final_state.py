# test_final_state.py
import os

def test_virtual_environment_exists():
    """Check that the virtual environment Python executable exists."""
    python_path = "/home/user/sim_env/bin/python"
    assert os.path.isfile(python_path), f"Virtual environment Python executable not found at {python_path}"
    assert os.access(python_path, os.X_OK), f"Python executable at {python_path} is not executable"

def test_script_exists():
    """Check that the simulation script was created."""
    script_path = "/home/user/run_sim.py"
    assert os.path.isfile(script_path), f"Simulation script not found at {script_path}"

def test_results_file_content():
    """Check that the results file exists and contains the correct statistical output."""
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    with open(results_path, "r") as f:
        content = f.read().strip()

    expected_content = "Mean: 7.9016, StdDev: 4.8878"
    assert content == expected_content, f"Results file content is incorrect. Expected '{expected_content}', but got '{content}'"