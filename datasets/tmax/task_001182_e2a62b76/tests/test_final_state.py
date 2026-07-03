# test_final_state.py

import os
import json
import pandas as pd
import numpy as np
import pytest

def test_final_state_csv_exists():
    csv_path = '/home/user/final_state.csv'
    assert os.path.isfile(csv_path), f"{csv_path} does not exist. The agent must save the final state here."

def test_mse_is_within_threshold():
    obs_path = '/home/user/observations.jsonl'
    assert os.path.isfile(obs_path), f"{obs_path} is missing."

    obs_x = []
    obs_u = []
    with open(obs_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            obs_x.append(data['coord_x'])
            obs_u.append(data['measured_pop_level'])

    agent_csv_path = '/home/user/final_state.csv'
    assert os.path.isfile(agent_csv_path), f"{agent_csv_path} is missing."

    try:
        agent_df = pd.read_csv(agent_csv_path)
    except Exception as e:
        pytest.fail(f"Failed to read {agent_csv_path} as a CSV: {e}")

    assert 'x' in agent_df.columns, "'x' column missing in final_state.csv"
    assert 'u' in agent_df.columns, "'u' column missing in final_state.csv"

    # Ensure the dataframe is sorted by x for proper interpolation
    agent_df = agent_df.sort_values(by='x')

    # Interpolate agent's output to the observation coordinates
    agent_u_interp = np.interp(obs_x, agent_df['x'], agent_df['u'])

    mse = np.mean((np.array(obs_u) - agent_u_interp)**2)

    assert mse <= 0.001, f"MSE is {mse:.6f}, which is greater than the threshold of 0.001"