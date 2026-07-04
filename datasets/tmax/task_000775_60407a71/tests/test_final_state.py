# test_final_state.py
import json
import os
import pytest

def get_ids(filepath):
    ids = set()
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    assert 'id' in data, "Missing 'id' in JSON"
                    assert 'tokens' in data, "Missing 'tokens' in JSON"
                    assert isinstance(data['tokens'], list), "'tokens' must be a list"
                    ids.add(data['id'])
    except AssertionError as e:
        pytest.fail(f"Schema validation failed: {e}")
    except Exception as e:
        pytest.fail(f"Failed to read or parse {filepath}: {e}")
    return ids

def test_cleaned_dataset_f1_score():
    output_file = '/home/user/cleaned_dataset.jsonl'
    ref_file = '/app/reference_ids.json'

    assert os.path.isfile(output_file), f"Output file {output_file} is missing. The pipeline may not have produced any output or saved it to the wrong location."
    assert os.path.isfile(ref_file), f"Reference file {ref_file} is missing."

    with open(ref_file, 'r') as f:
        ground_truth_ids = set(json.load(f))

    agent_ids = get_ids(output_file)

    assert len(agent_ids) > 0, "No records found in output file. The pipeline may have dropped all records."

    true_positives = len(agent_ids.intersection(ground_truth_ids))
    false_positives = len(agent_ids - ground_truth_ids)
    false_negatives = len(ground_truth_ids - agent_ids)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.95, f"F1 Score {f1:.4f} is less than the required threshold of 0.95. Precision: {precision:.4f}, Recall: {recall:.4f}"