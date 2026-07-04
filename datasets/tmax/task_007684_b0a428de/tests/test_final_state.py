# test_final_state.py
import os

def test_query_graph_script_exists():
    """Test that the query_graph.py script was created."""
    script_path = '/home/user/query_graph.py'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

def test_pattern_results_content():
    """Test that pattern_results.txt contains the correct output."""
    results_path = '/home/user/pattern_results.txt'
    assert os.path.isfile(results_path), f"The output file {results_path} is missing."

    with open(results_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["Initech", "TechCorp"]

    assert lines == expected_lines, (
        f"The contents of {results_path} are incorrect.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {lines}"
    )