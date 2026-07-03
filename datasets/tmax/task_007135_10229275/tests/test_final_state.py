# test_final_state.py
import os

def test_prepare_data_script_exists():
    path = '/home/user/prepare_data.py'
    assert os.path.exists(path), f"Expected script {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_corrected_features_csv():
    path = '/home/user/corrected_features.csv'
    assert os.path.exists(path), f"Expected output file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 5, f"{path} does not contain enough lines."
    assert lines[0] == "y_obs,x_pred,iterations", f"Header in {path} is incorrect."

    expected_prefixes = [
        "1.7,1.0000,",
        "4.6,2.0000,",
        "18.8,4.0000,",
        "24.832,4.6000,"
    ]

    for i, prefix in enumerate(expected_prefixes):
        line = lines[i + 1]
        assert line.startswith(prefix), f"Line {i + 2} in {path} expected to start with '{prefix}', but got '{line}'"

        # Check that iterations is an integer
        parts = line.split(',')
        assert len(parts) == 3, f"Line {i + 2} does not have exactly 3 columns."
        try:
            iterations = int(parts[2])
            assert iterations > 0, f"Iterations must be greater than 0, got {iterations} on line {i + 2}"
        except ValueError:
            assert False, f"Iterations column on line {i + 2} is not an integer: {parts[2]}"