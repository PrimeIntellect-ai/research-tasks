# test_final_state.py

import os
import json
import math
import csv

def test_summary_json_exists():
    """Test that the summary.json file was created."""
    assert os.path.isfile('/home/user/summary.json'), "The file /home/user/summary.json does not exist."

def test_summary_json_content():
    """Test that summary.json contains the correct structure and accurately computed counts."""
    summary_path = '/home/user/summary.json'

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{summary_path} is not a valid JSON file."

    assert "distribution" in data, "The key 'distribution' is missing from the JSON."
    dist = data["distribution"]

    assert "exact" in dist, "The key 'exact' is missing from 'distribution'."
    assert "under" in dist, "The key 'under' is missing from 'distribution'."
    assert "over" in dist, "The key 'over' is missing from 'distribution'."

    # Recompute the expected distribution based on the actual files
    reference_data = {}
    ref_path = '/home/user/reference.csv'
    assert os.path.isfile(ref_path), f"Reference file {ref_path} is missing."

    with open(ref_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            reference_data[row['run_id']] = float(row['expected_sum'])

    expected_exact = 0
    expected_under = 0
    expected_over = 0

    for i in range(1, 21):
        run_id = f'run_{i}'
        output_file = f'/home/user/sim_runs/{run_id}/output.dat'

        assert os.path.isfile(output_file), f"Simulation output file {output_file} is missing."

        with open(output_file, 'r') as f:
            numbers = [float(line.strip()) for line in f if line.strip()]

        computed_sum = math.fsum(numbers)
        expected_sum = reference_data[run_id]

        diff = computed_sum - expected_sum
        if diff == 0.0:
            expected_exact += 1
        elif diff < 0.0:
            expected_under += 1
        else:
            expected_over += 1

    assert dist["exact"] == expected_exact, f"Expected 'exact' count to be {expected_exact}, but got {dist['exact']}."
    assert dist["under"] == expected_under, f"Expected 'under' count to be {expected_under}, but got {dist['under']}."
    assert dist["over"] == expected_over, f"Expected 'over' count to be {expected_over}, but got {dist['over']}."