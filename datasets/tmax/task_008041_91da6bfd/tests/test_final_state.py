# test_final_state.py
import os

def test_eigen_baseline_file_exists():
    """Verify that the output file eigen_baseline.txt is created."""
    file_path = '/home/user/eigen_baseline.txt'
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} exists but is not a file."

def test_eigen_baseline_content():
    """Verify the content of eigen_baseline.txt matches the expected mean largest eigenvalue."""
    file_path = '/home/user/eigen_baseline.txt'
    assert os.path.exists(file_path), f"The file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content, "The file eigen_baseline.txt is empty."

    try:
        value = float(content)
    except ValueError:
        raise AssertionError(f"The content of eigen_baseline.txt ('{content}') is not a valid float.")

    # The expected value is approximately 9.0766. 
    # We allow a small tolerance due to potential numpy version differences.
    expected_value = 9.0766
    tolerance = 0.005

    assert abs(value - expected_value) <= tolerance, \
        f"The calculated mean eigenvalue {value} is not within the acceptable range of {expected_value} +/- {tolerance}."

def test_bootstrap_pca_script_exists():
    """Verify that the student's script bootstrap_pca.py exists."""
    script_path = '/home/user/bootstrap_pca.py'
    assert os.path.exists(script_path), f"The script {script_path} is missing."
    assert os.path.isfile(script_path), f"The path {script_path} exists but is not a file."