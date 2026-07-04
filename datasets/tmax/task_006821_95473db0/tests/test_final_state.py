# test_final_state.py
import os
import re

def test_parquet_file_exists_and_valid():
    file_path = '/home/user/processed_papers.parquet'
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, 'rb') as f:
        header = f.read(4)
        f.seek(-4, os.SEEK_END)
        footer = f.read(4)

    assert header == b'PAR1', f"File {file_path} does not have a valid Parquet header."
    assert footer == b'PAR1', f"File {file_path} does not have a valid Parquet footer."

def test_best_alpha():
    file_path = '/home/user/best_alpha.txt'
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == '1.0', f"Expected best alpha to be '1.0', got '{content}'"

def test_metrics():
    file_path = '/home/user/metrics.txt'
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines in metrics.txt, got {len(lines)}"

    expected_categories = ['math.AG', 'math.CO', 'math.PR']
    pattern = re.compile(r"^Category: (math\.(?:AG|CO|PR)), Avg_Length: (\d+\.\d{2})$")

    actual_categories = []
    for line in lines:
        match = pattern.match(line)
        assert match, f"Line format incorrect: '{line}'. Expected 'Category: {{category}}, Avg_Length: {{avg_length:.2f}}'"
        actual_categories.append(match.group(1))

    assert actual_categories == expected_categories, f"Categories not sorted alphabetically or missing. Expected {expected_categories}, got {actual_categories}"

    # Check exact values derived from the known data and random state
    expected_lines = [
        "Category: math.AG, Avg_Length: 30.60",
        "Category: math.CO, Avg_Length: 29.86",
        "Category: math.PR, Avg_Length: 32.75"
    ]

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'"