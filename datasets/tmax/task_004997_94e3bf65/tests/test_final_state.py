# test_final_state.py
import json
import os
import pytest

def test_output_jsonl_exists_and_metric():
    agent_file = '/home/user/etl/output.jsonl'
    assert os.path.isfile(agent_file), f"Expected output file not found at {agent_file}"

    expected = {
        (0, "hello"), (0, "thank"), (0, "you"), (0, "for"), (0, "calling"), (0, "support"),
        (0, "my"), (0, "account"), (0, "is"), (0, "locked"), (0, "and"), (0, "i"), (0, "cannot"),
        (10, "login"), (10, "to"), (10, "the"), (10, "system"), (10, "i"), (10, "understand"),
        (10, "let"), (10, "me"), (10, "help"), (10, "you"), (20, "unlock"), (20, "the"), (20, "account")
    }

    agent_data = set()
    try:
        with open(agent_file, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    agent_data.add((row['bucket_start'], row['word']))
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON at line {line_number} in {agent_file}: {line}")
                except KeyError as e:
                    pytest.fail(f"Missing key {e} in JSON at line {line_number} in {agent_file}: {line}")
    except Exception as e:
        pytest.fail(f"Failed to read or parse {agent_file}: {e}")

    intersection = len(expected.intersection(agent_data))
    union = len(expected.union(agent_data))

    assert union > 0, "No valid (bucket_start, word) pairs found in the output."

    score = intersection / union
    threshold = 0.70

    assert score >= threshold, (
        f"Jaccard similarity score {score:.3f} is below the threshold of {threshold:.3f}. "
        f"Intersection size: {intersection}, Union size: {union}."
    )