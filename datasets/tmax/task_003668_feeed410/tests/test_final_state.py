# test_final_state.py
import os
import math

def test_results_file_exists():
    results_path = "/home/user/sim_project/results.csv"
    assert os.path.isfile(results_path), f"File {results_path} does not exist. Ensure the notebook was executed successfully."

def test_results_content():
    results_path = "/home/user/sim_project/results.csv"
    assert os.path.isfile(results_path), "Results file missing."

    with open(results_path, 'r') as f:
        content = f.read().strip()

    assert content, f"File {results_path} is empty."

    parts = content.split(',')
    assert len(parts) == 3, f"Expected exactly 3 comma-separated values in {results_path}, but got {len(parts)}."

    try:
        results = [float(x) for x in parts]
    except ValueError:
        assert False, f"Could not parse values in {results_path} as floats. Content: {content}"

    expected = [0.749558, 0.749558, 0.500057]

    for i, (res, exp) in enumerate(zip(results, expected)):
        assert math.isclose(res, exp, abs_tol=1e-2), (
            f"Estimated parameter at index {i} is {res}, expected approximately {exp} "
            "(tolerance 1e-2). Ensure you are handling collinearity properly."
        )