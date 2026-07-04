# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_scores_csv_exists():
    path = "/app/output/scores.csv"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

def test_scores_mse_threshold():
    output_path = "/app/output/scores.csv"
    input_path = "/app/data/input.csv"

    assert os.path.isfile(output_path), f"Agent output file not found at {output_path}"
    assert os.path.isfile(input_path), f"Input data file not found at {input_path}"

    try:
        agent_df = pd.read_csv(output_path)
    except Exception as e:
        pytest.fail(f"Failed to read {output_path} as CSV: {e}")

    assert 'score' in agent_df.columns, f"Column 'score' not found in {output_path}"

    try:
        raw_df = pd.read_csv(input_path)
    except Exception as e:
        pytest.fail(f"Failed to read {input_path} as CSV: {e}")

    def parse_val(v):
        if isinstance(v, str):
            v = v.replace('D', 'E')
        return float(v)

    truth_scores = []
    for _, row in raw_df.iterrows():
        x = parse_val(row['x'])
        y = parse_val(row['y'])
        alpha = 0.00845
        score = (x * y) / (x - y + alpha)
        truth_scores.append(score)

    agent_scores = agent_df['score'].values
    truth_scores = np.array(truth_scores)

    assert len(agent_scores) == len(truth_scores), (
        f"Length mismatch: Agent provided {len(agent_scores)} scores, "
        f"but expected {len(truth_scores)} scores based on input."
    )

    mse = np.mean((agent_scores - truth_scores)**2)
    threshold = 1e-5

    assert mse <= threshold, (
        f"MSE too high! Measured MSE: {mse:.8f}, Threshold: {threshold}. "
        "Check if the legacy exponent format ('D') was correctly parsed and "
        "the correct alpha value (0.00845) was used."
    )