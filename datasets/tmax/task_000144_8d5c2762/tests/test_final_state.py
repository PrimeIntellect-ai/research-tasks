# test_final_state.py
import os
import math

def test_final_state():
    final_state_path = "/home/user/final_state.txt"
    truth_state_path = "/home/user/.truth_state"

    assert os.path.isfile(final_state_path), f"The output file {final_state_path} is missing."
    assert os.path.isfile(truth_state_path), f"The truth file {truth_state_path} is missing."

    with open(final_state_path, "r") as f:
        student_state = f.read().strip()

    with open(truth_state_path, "r") as f:
        truth_state = f.read().strip()

    try:
        student_vals = [float(x) for x in student_state.split(",")]
    except ValueError:
        assert False, f"Could not parse student output as comma-separated floats: {student_state}"

    try:
        truth_vals = [float(x) for x in truth_state.split(",")]
    except ValueError:
        assert False, f"Could not parse truth output as comma-separated floats: {truth_state}"

    assert len(student_vals) == 3, f"Expected 3 comma-separated values (A, mu, sigma), got {len(student_vals)}"
    assert len(truth_vals) == 3, "Truth file is malformed"

    labels = ["A", "mu", "sigma"]
    for i, (s, t) in enumerate(zip(student_vals, truth_vals)):
        assert math.isclose(s, t, abs_tol=5e-3), f"Parameter {labels[i]} value {s} does not match expected {t} within tolerance."