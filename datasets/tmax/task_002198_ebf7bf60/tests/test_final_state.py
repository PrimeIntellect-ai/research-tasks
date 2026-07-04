# test_final_state.py

import os
import json
import pytest

def test_result_file_exists():
    path = '/home/user/result.json'
    assert os.path.isfile(path), f"Expected result file at {path} is missing."

def test_result_format_and_metric():
    path = '/home/user/result.json'
    assert os.path.isfile(path), "Result file missing."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert 'peaks' in data, "The key 'peaks' is missing from the JSON output."
    peaks = data['peaks']
    assert isinstance(peaks, list), "'peaks' should be a list."
    assert len(peaks) == 3, f"Expected exactly 3 peaks, but found {len(peaks)}."

    extracted_means = []
    for i, peak in enumerate(peaks):
        assert isinstance(peak, dict), f"Peak at index {i} is not a dictionary."
        assert 'mean_index' in peak, f"Peak at index {i} is missing 'mean_index'."
        assert 'ci_lower' in peak, f"Peak at index {i} is missing 'ci_lower'."
        assert 'ci_upper' in peak, f"Peak at index {i} is missing 'ci_upper'."

        extracted_means.append(peak['mean_index'])

    true_means = [40, 90, 160]

    mae = sum(abs(e - t) for e, t in zip(extracted_means, true_means)) / 3.0

    assert mae <= 3.0, f"MAE {mae} exceeds threshold 3.0. Extracted means: {extracted_means}, Expected means: {true_means}"