# test_final_state.py

import os
import json
import pytest

PIPELINE_RUNS_PATH = '/home/user/pipeline_runs.jsonl'
EXPECTED_CONFIGS = {
    (42, 1.0),
    (42, 0.1),
    (99, 1.0)
}

def test_pipeline_runs_exists():
    assert os.path.exists(PIPELINE_RUNS_PATH), f"The file {PIPELINE_RUNS_PATH} does not exist."
    assert os.path.isfile(PIPELINE_RUNS_PATH), f"The path {PIPELINE_RUNS_PATH} is not a file."

def test_pipeline_runs_content():
    assert os.path.exists(PIPELINE_RUNS_PATH), f"The file {PIPELINE_RUNS_PATH} does not exist."

    with open(PIPELINE_RUNS_PATH, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 3, f"Expected exactly 3 lines in {PIPELINE_RUNS_PATH}, found {len(lines)}."

    found_configs = set()
    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {PIPELINE_RUNS_PATH} is not valid JSON.")

        assert "seed" in record, f"Line {i+1} missing 'seed' key."
        assert "C" in record, f"Line {i+1} missing 'C' key."
        assert "accuracy" in record, f"Line {i+1} missing 'accuracy' key."

        seed = record["seed"]
        c_val = record["C"]
        accuracy = record["accuracy"]

        assert isinstance(seed, int), f"Line {i+1}: 'seed' must be an integer."
        assert isinstance(c_val, (int, float)), f"Line {i+1}: 'C' must be a float."
        assert isinstance(accuracy, (int, float)), f"Line {i+1}: 'accuracy' must be a float."

        assert 0.0 <= accuracy <= 1.0, f"Line {i+1}: 'accuracy' must be between 0.0 and 1.0."

        # Convert C to float for comparison
        found_configs.add((seed, float(c_val)))

    missing_configs = EXPECTED_CONFIGS - found_configs
    extra_configs = found_configs - EXPECTED_CONFIGS

    assert not missing_configs, f"Missing expected experiment configurations: {missing_configs}"
    assert not extra_configs, f"Found unexpected experiment configurations: {extra_configs}"