# test_final_state.py

import os
import json
import stat
from collections import defaultdict

def test_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    script_path = "/home/user/process_graph.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_output_json_correctness():
    """Test that the output JSON file contains the correct top 3 targets."""
    input_path = "/home/user/server_logs.jsonl"
    output_path = "/home/user/top_targets.json"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    # Compute expected output
    in_degrees = defaultdict(int)
    with open(input_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get("status") == "OK":
                target = record.get("target")
                if target:
                    in_degrees[target] += 1

    # Sort by in_degree desc, then server name asc
    sorted_targets = sorted(in_degrees.items(), key=lambda x: (-x[1], x[0]))
    top_3 = sorted_targets[:3]

    expected_output = [{"server": server, "in_degree": count} for server, count in top_3]

    # Read actual output
    with open(output_path, "r") as f:
        try:
            actual_output = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Output file {output_path} is not valid JSON."

    assert isinstance(actual_output, list), f"Output in {output_path} must be a JSON array."
    assert len(actual_output) == len(expected_output), f"Expected {len(expected_output)} items, got {len(actual_output)}."

    for i, (expected, actual) in enumerate(zip(expected_output, actual_output)):
        assert actual == expected, f"Mismatch at index {i}: expected {expected}, got {actual}."