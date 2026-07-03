# test_final_state.py
import os

def test_results_file_exists():
    """Check if the results.txt file was created."""
    file_path = '/home/user/results.txt'
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you run the Rust program?"

def test_results_content():
    """Verify the contents of results.txt match the expected Kahan summation output."""
    file_path = '/home/user/results.txt'

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 11, f"Expected exactly 11 lines of output, but found {len(lines)}."

    val = 1.23456e-4
    expected_lines = []

    # Line 1: Total sum
    expected_lines.append(f"{val * 1000000:.4f}")

    # Lines 2 to 11: Running sum at every 100,000th element
    for i in range(1, 11):
        expected_lines.append(f"{val * (i * 100000):.4f}")

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} is incorrect. Expected '{expected}', got '{actual}'. This indicates precision loss or incorrect formatting."