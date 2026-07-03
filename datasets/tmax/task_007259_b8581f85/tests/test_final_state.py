# test_final_state.py
import os
import json

def test_analyze_graph_go_exists():
    path = "/home/user/analyze_graph.go"
    assert os.path.isfile(path), f"File {path} is missing. Did you create the Go program?"

def test_matches_json_correctness():
    path = "/home/user/matches.json"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the Go program to generate the output?"

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} does not contain valid JSON."

    assert isinstance(data, list), f"The JSON output in {path} must be a list (array)."

    expected_data = [
        {
            "company": "TechCorp",
            "industry": "AI",
            "person": "Alice"
        },
        {
            "company": "FutureAI",
            "industry": "AI",
            "person": "Bob"
        },
        {
            "company": "FutureAI",
            "industry": "AI",
            "person": "Charlie"
        }
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} matches, but got {len(data)}."

    for i, expected_match in enumerate(expected_data):
        assert data[i] == expected_match, f"Match at index {i} is incorrect. Expected {expected_match}, got {data[i]}."

def test_matches_json_formatting():
    path = "/home/user/matches.json"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read()

    # Check for 2-space indentation by looking at the first few lines
    lines = content.splitlines()
    if len(lines) > 2:
        # The second line should start with exactly two spaces and then a quote or brace
        assert lines[1].startswith("  ") and not lines[1].startswith("   "), "The JSON file does not appear to be formatted with 2-space indentation."