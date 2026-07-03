# test_final_state.py
import os
import difflib

def read_clean(path):
    try:
        with open(path, 'r') as f:
            return '\n'.join([line.strip() for line in f if line.strip()])
    except Exception:
        return ""

def test_parser_recovered():
    """Check if the parser.sh script was recovered to the correct location."""
    assert os.path.exists('/home/user/parser.sh'), "/home/user/parser.sh was not recovered from the backup image."

def test_summary_csv_similarity():
    """Evaluate the accuracy of the generated summary.csv against the expected truth."""
    expected_path = '/app/.truth/expected.csv'
    actual_path = '/home/user/summary.csv'

    assert os.path.exists(actual_path), f"Output file {actual_path} does not exist. Did you run the parser and save the output?"
    assert os.path.exists(expected_path), f"Truth file {expected_path} does not exist in the environment."

    expected = read_clean(expected_path)
    actual = read_clean(actual_path)

    ratio = difflib.SequenceMatcher(None, expected, actual).ratio()
    threshold = 0.85

    assert ratio >= threshold, (
        f"Summary CSV accuracy is too low. "
        f"Similarity ratio {ratio:.4f} is below the required threshold of {threshold}."
    )