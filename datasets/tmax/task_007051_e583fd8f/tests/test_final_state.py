# test_final_state.py
import os
import re
import ast

def test_fixed_result_exists():
    path = '/home/user/fixed_result.txt'
    assert os.path.isfile(path), f"Expected output file {path} is missing."

def test_fixed_result_format_and_content():
    path = '/home/user/fixed_result.txt'
    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "The file should contain at least two lines for Test Score and Best Params."

    score_line = lines[0]
    params_line = lines[1]

    assert score_line.startswith("Test Score:"), "The first line must start with 'Test Score:'"
    assert params_line.startswith("Best Params:"), "The second line must start with 'Best Params:'"

    # Check if Test Score is correctly formatted (4 decimal places)
    score_match = re.search(r'Test Score:\s*([0-9]+\.[0-9]{4})$', score_line)
    assert score_match is not None, "Test Score must be a number rounded to exactly 4 decimal places."

    # Check if Best Params contains the required keys
    params_str = params_line.replace("Best Params:", "").strip()
    try:
        params_dict = ast.literal_eval(params_str)
        assert isinstance(params_dict, dict), "Best Params must be a valid Python dictionary."
        assert 'tfidf__max_features' in params_dict, "Best Params dictionary is missing 'tfidf__max_features'."
        assert 'knn__n_neighbors' in params_dict, "Best Params dictionary is missing 'knn__n_neighbors'."

        # Verify the tuned values are from the specified grid
        assert params_dict['tfidf__max_features'] in [50, 100], "tfidf__max_features must be chosen from [50, 100]."
        assert params_dict['knn__n_neighbors'] in [3, 5, 7], "knn__n_neighbors must be chosen from [3, 5, 7]."
    except (SyntaxError, ValueError):
        assert False, "The Best Params output is not a valid dictionary representation."