# test_final_state.py

import os
import numpy as np
import pandas as pd
import pytest

def test_sim_results_exists_and_format():
    results_path = '/home/user/sim_results.csv'
    assert os.path.isfile(results_path), f"File {results_path} does not exist."

    df = pd.read_csv(results_path)
    assert 't' in df.columns, "Column 't' missing from sim_results.csv"
    assert 'x' in df.columns, "Column 'x' missing from sim_results.csv"
    assert 'v' in df.columns, "Column 'v' missing from sim_results.csv"
    assert len(df) >= 2001, f"Expected at least 2001 rows, got {len(df)}"

def test_sim_results_accuracy():
    results_path = '/home/user/sim_results.csv'
    assert os.path.isfile(results_path), f"File {results_path} does not exist."

    df = pd.read_csv(results_path)

    # Generate truth
    t_val = 0.0
    x_val = 2.0
    v_val = 0.0
    dt = 0.01
    omega = 1.5
    gamma = 0.2
    alpha = 0.1

    truth_x = []
    for i in range(2001):
        truth_x.append(x_val)

        k1_x = v_val
        k1_v = -gamma*v_val - omega*omega*x_val - alpha*x_val**3

        x2 = x_val + 0.5*dt*k1_x
        v2 = v_val + 0.5*dt*k1_v
        k2_x = v2
        k2_v = -gamma*v2 - omega*omega*x2 - alpha*x2**3

        x3 = x_val + 0.5*dt*k2_x
        v3 = v_val + 0.5*dt*k2_v
        k3_x = v3
        k3_v = -gamma*v3 - omega*omega*x3 - alpha*x3**3

        x4 = x_val + dt*k3_x
        v4 = v_val + dt*k3_v
        k4_x = v4
        k4_v = -gamma*v4 - omega*omega*x4 - alpha*x4**3

        x_val += (dt/6.0)*(k1_x + 2*k2_x + 2*k3_x + k4_x)
        v_val += (dt/6.0)*(k1_v + 2*k2_v + 2*k3_v + k4_v)

    truth_x = np.array(truth_x)
    agent_x = df['x'].values[:2001]

    mse = np.mean((truth_x - agent_x)**2)
    rmse = np.sqrt(mse)

    threshold = 1e-4
    assert rmse < threshold, f"RMSE {rmse} is not less than threshold {threshold}"