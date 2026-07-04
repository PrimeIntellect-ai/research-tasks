# test_final_state.py

import os
import json

def test_cleaned_sample_metric():
    # Check if the pipeline script was created
    assert os.path.exists('/home/user/pipeline.py'), "Expected script /home/user/pipeline.py does not exist."

    # Check if the output file was created
    output_file = '/home/user/cleaned_sample.json'
    assert os.path.exists(output_file), f"Expected output file {output_file} does not exist."

    try:
        with open(output_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        assert False, f"Failed to parse {output_file} as JSON: {e}"

    assert isinstance(data, list), "Output JSON must be an array of objects."

    selected_ids = [d.get('id') for d in data if 'id' in d]
    assert len(selected_ids) > 0, "No valid records with 'id' found in cleaned_sample.json."

    valid = sum(1 for x in selected_ids if x <= 35000)
    invalid = sum(1 for x in selected_ids if x > 35000)
    duplicates = len(selected_ids) - len(set(selected_ids))

    expected_count = 7000

    score = 1.0
    if invalid > 0:
        score -= (invalid / len(selected_ids))
    if duplicates > 0:
        score -= (duplicates / len(selected_ids))

    count_diff = abs(len(selected_ids) - expected_count)
    if count_diff > 500:
        score -= 0.5
    elif count_diff > 100:
        score -= 0.2

    score = max(0.0, score)

    assert score >= 0.95, (
        f"Metric threshold failed: score {score:.3f} < 0.95. "
        f"Total records: {len(selected_ids)}, Invalid (>35000): {invalid}, "
        f"Duplicates: {duplicates}, Expected count: {expected_count}."
    )