# test_final_state.py

import os

def test_samples_txt_exists_and_valid():
    """Test that the notebook was executed and generated samples.txt correctly."""
    path = "/home/user/samples.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The notebook may not have been executed."

    with open(path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 10000, f"Expected 10000 lines in {path}, found {len(lines)}."

def test_evaluate_py_exists():
    """Test that the evaluate.py script was created."""
    path = "/home/user/evaluate.py"
    assert os.path.isfile(path), f"Script {path} was not created."

def test_convergence_csv_matches_expected():
    """Test that convergence.csv has the correct KS statistics."""
    path = "/home/user/convergence.csv"
    assert os.path.isfile(path), f"Output file {path} was not created."

    expected_content = (
        "N,KS\n"
        "1000,0.0154\n"
        "5000,0.0097\n"
        "10000,0.0084\n"
    )

    with open(path, 'r') as f:
        content = f.read()

    # Normalize line endings and strip trailing whitespace for robust comparison
    content_normalized = content.strip().replace('\r\n', '\n')
    expected_normalized = expected_content.strip()

    assert content_normalized == expected_normalized, (
        f"Content of {path} does not match expected output.\n"
        f"Expected:\n{expected_normalized}\n"
        f"Got:\n{content_normalized}"
    )