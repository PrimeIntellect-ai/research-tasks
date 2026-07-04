# test_final_state.py

import os
import pytest

def load_data(filepath):
    lines = set()
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.add(line)
    except Exception:
        pass
    return lines

def test_script_exists_and_executable():
    script_path = "/home/user/run_etl.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_output_exists():
    output_path = "/home/user/final_output.csv"
    assert os.path.isfile(output_path), f"Final output file not found at {output_path}"

def test_match_ratio():
    golden_path = "/opt/evaluation/golden_output.csv"
    agent_path = "/home/user/final_output.csv"

    assert os.path.isfile(golden_path), f"Golden output file missing: {golden_path}"

    golden = load_data(golden_path)
    agent = load_data(agent_path)

    assert len(golden) > 0, "Golden dataset is empty, cannot compute match ratio."

    intersection = golden.intersection(agent)
    match_ratio = len(intersection) / len(golden)

    threshold = 0.95
    assert match_ratio >= threshold, (
        f"Match ratio {match_ratio:.4f} is below the threshold of {threshold}. "
        f"Matched {len(intersection)} out of {len(golden)} expected rows."
    )