# test_final_state.py

import os
import pytest
import pandas as pd
from sklearn.metrics import mean_squared_error

def test_pagerank_results():
    output_path = '/home/user/pagerank_results.csv'
    golden_path = '/app/golden_pagerank.csv'

    assert os.path.isfile(output_path), f"Agent output file not found: {output_path}"
    assert os.path.isfile(golden_path), f"Golden reference file not found: {golden_path}"

    try:
        agent_df = pd.read_csv(output_path)
    except Exception as e:
        pytest.fail(f"Failed to read agent output CSV: {e}")

    assert 'node_id' in agent_df.columns, "Column 'node_id' missing in agent output"
    assert 'pagerank_score' in agent_df.columns, "Column 'pagerank_score' missing in agent output"

    agent_df = agent_df.set_index('node_id')
    golden_df = pd.read_csv(golden_path).set_index('node_id')

    # Align dataframes
    merged = agent_df.join(golden_df, lsuffix='_agent', rsuffix='_gold').fillna(0)

    # Compute MSE
    mse = mean_squared_error(merged['pagerank_score_gold'], merged['pagerank_score_agent'])

    threshold = 0.0001
    assert mse <= threshold, f"MSE {mse} exceeds threshold of {threshold}"