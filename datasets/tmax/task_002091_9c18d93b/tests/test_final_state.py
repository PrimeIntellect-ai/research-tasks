# test_final_state.py
import os
import csv
import math

def test_results_csv_exists():
    assert os.path.isfile('/home/user/results.csv'), "The file /home/user/results.csv does not exist."

def test_results_csv_content():
    expected_exact = [0.2443, 0.1765, 0.2312, 0.1601, 0.1879]

    with open('/home/user/results.csv', 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, "results.csv is empty."

        assert header == ['Node', 'Exact', 'Empirical'], f"Incorrect CSV header: {header}"

        rows = list(reader)
        assert len(rows) == 5, f"Expected exactly 5 data rows, but found {len(rows)}."

        for i, row in enumerate(rows):
            assert len(row) == 3, f"Row {i} has {len(row)} columns instead of 3."

            try:
                node = int(row[0])
            except ValueError:
                assert False, f"Node value '{row[0]}' is not an integer."

            assert node == i, f"Expected Node {i}, but got {node}."

            # Check exactly 4 decimal places
            exact_str = row[1]
            empirical_str = row[2]

            assert '.' in exact_str and len(exact_str.split('.')[1]) == 4, f"Exact value '{exact_str}' is not formatted to exactly 4 decimal places."
            assert '.' in empirical_str and len(empirical_str.split('.')[1]) == 4, f"Empirical value '{empirical_str}' is not formatted to exactly 4 decimal places."

            exact_val = float(exact_str)
            empirical_val = float(empirical_str)

            exact_diff = abs(exact_val - expected_exact[i])
            assert exact_diff <= 0.0002, f"Exact value for node {i} ({exact_val}) differs from expected ({expected_exact[i]}) by more than 0.0002."

            emp_diff = abs(empirical_val - expected_exact[i])
            assert emp_diff <= 0.005, f"Empirical value for node {i} ({empirical_val}) differs from expected ({expected_exact[i]}) by more than 0.005. MCMC might not have converged or logic is incorrect."

def test_source_code_exists():
    assert os.path.isfile('/home/user/pagerank.cpp'), "The source code file /home/user/pagerank.cpp does not exist."