# test_final_state.py
import os
import pytest

BEST_PARAMS_PATH = "/home/user/best_params.txt"
CPP_PATH = "/home/user/lv_fit.cpp"
SH_PATH = "/home/user/grid_search.sh"

def test_files_exist():
    """Test that the required source and output files exist."""
    assert os.path.exists(CPP_PATH), f"Missing required file: {CPP_PATH}"
    assert os.path.exists(SH_PATH), f"Missing required file: {SH_PATH}"
    assert os.path.exists(BEST_PARAMS_PATH), f"Missing required file: {BEST_PARAMS_PATH}"

def test_best_params_content():
    """Test that best_params.txt contains the correct parameters and a small MSE."""
    with open(BEST_PARAMS_PATH, 'r') as f:
        content = f.read().strip()

    assert content, "best_params.txt is empty"

    parts = content.split(',')
    assert len(parts) == 5, f"best_params.txt must contain exactly 5 comma-separated values (alpha,beta,gamma,delta,MSE), got {len(parts)}"

    try:
        alpha = float(parts[0])
        beta = float(parts[1])
        gamma = float(parts[2])
        delta = float(parts[3])
        mse = float(parts[4])
    except ValueError:
        pytest.fail(f"Could not parse values in best_params.txt as floats. Content was: {content}")

    assert alpha == 1.5, f"Expected alpha=1.5, got {alpha}"
    assert beta == 1.0, f"Expected beta=1.0, got {beta}"
    assert gamma == 3.0, f"Expected gamma=3.0, got {gamma}"
    assert delta == 1.0, f"Expected delta=1.0, got {delta}"
    assert mse < 1e-5, f"Expected MSE < 1e-5, got {mse}"