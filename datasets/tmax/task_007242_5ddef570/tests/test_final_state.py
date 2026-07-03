# test_final_state.py

import os

def test_pca_ci_file_exists():
    """Verify that the output file pca_ci.txt was created."""
    file_path = "/home/user/pca_ci.txt"
    assert os.path.isfile(file_path), f"Output file not found: {file_path}"

def test_pca_ci_content():
    """Verify that the output file contains the correct bootstrapped confidence intervals."""
    file_path = "/home/user/pca_ci.txt"
    with open(file_path, "r") as f:
        content = f.read().strip()

    # The expected output is deterministic based on the provided setup script's seed
    # and the specific bootstrap parameters (1000 iterations, random seeds 0-999).
    expected = "0.4578,0.5401"

    assert content == expected, (
        f"Incorrect confidence interval in {file_path}. "
        f"Expected '{expected}', but got '{content}'."
    )