# test_final_state.py
import os

def test_venv_exists():
    """Check that the virtual environment was created."""
    venv_python = "/home/user/venv/bin/python"
    assert os.path.exists(venv_python), f"Virtual environment python not found at {venv_python}"

def test_script_exists():
    """Check that the script was created."""
    script_path = "/home/user/mc_evo.py"
    assert os.path.exists(script_path), f"Script not found at {script_path}"

def test_fit_result():
    """Check that the output file exists and contains a valid k value."""
    result_path = "/home/user/fit_result.txt"
    assert os.path.exists(result_path), f"Result file not found at {result_path}"

    with open(result_path, "r") as f:
        content = f.read().strip()

    try:
        k = float(content)
    except ValueError:
        assert False, f"Could not parse '{content}' as a float in {result_path}"

    assert 0.0130 <= k <= 0.0136, f"Fitted k={k} is outside the expected range [0.0130, 0.0136]"