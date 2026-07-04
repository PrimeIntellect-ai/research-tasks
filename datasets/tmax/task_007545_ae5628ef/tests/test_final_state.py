# test_final_state.py
import os

def test_result_file_exists():
    """Check if the result file was created."""
    file_path = '/home/user/result.txt'
    assert os.path.isfile(file_path), f"Output file is missing: {file_path}"

def test_result_file_contents():
    """Check if the contents of the result file match the expected computation."""
    file_path = '/home/user/result.txt'

    # Compute the expected ground truth
    arr = [0.2, 0.8, 0.4, 0.9, 0.3, 0.7, 0.5, 0.6, 0.1, 0.9]
    diff = 1.0

    while diff >= 0.0001:
        new_arr = list(arr)
        for i in range(1, 9):
            new_arr[i] = 0.5 * arr[i] + 0.25 * arr[i-1] + 0.25 * arr[i+1]

        diff = max(abs(new_arr[i] - arr[i]) for i in range(10))
        arr = new_arr

    mean_val = sum(arr) / len(arr)
    expected_line1 = f"Mean: {mean_val:.4f}"
    expected_line2 = "Hypothesis: H1" if mean_val > 0.45 else "Hypothesis: H0"

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in result.txt, but found {len(lines)}."
    assert lines[0] == expected_line1, f"Line 1 mismatch. Expected '{expected_line1}', got '{lines[0]}'."
    assert lines[1] == expected_line2, f"Line 2 mismatch. Expected '{expected_line2}', got '{lines[1]}'."