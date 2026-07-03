# test_final_state.py
import os
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

def test_simulation_csv_exists_and_format():
    csv_path = "/home/user/simulation.csv"
    assert os.path.exists(csv_path), f"Expected output file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

    df = pd.read_csv(csv_path)
    expected_columns = {'time', 'theta', 'theta_dot'}
    assert expected_columns.issubset(df.columns), f"CSV must contain columns {expected_columns}, found {list(df.columns)}"

    frames = 300
    assert len(df) >= frames, f"CSV must contain at least {frames} rows, found {len(df)}."

def test_simulation_accuracy():
    csv_path = "/home/user/simulation.csv"
    assert os.path.exists(csv_path), "Simulation CSV missing, cannot check accuracy."

    # Ground truth parameters
    g = 9.81
    L = 2.5
    b = 0.15
    duration = 10
    fps = 30
    frames = fps * duration

    t_eval = np.linspace(0, duration, frames, endpoint=False)

    def pendulum_ode(t, y):
        return [y[1], -(g/L)*np.sin(y[0]) - b*y[1]]

    # Recompute ground truth
    sol = solve_ivp(
        pendulum_ode, 
        [0, duration], 
        [1.0, 0.0], 
        t_eval=t_eval, 
        method='RK45', 
        rtol=1e-8, 
        atol=1e-8
    )
    true_theta = sol.y[0]

    # Load agent data
    df = pd.read_csv(csv_path)
    assert 'theta' in df.columns, "Column 'theta' missing from CSV."

    agent_theta = df['theta'].values[:frames]
    assert len(agent_theta) == frames, f"Expected at least {frames} valid theta values."

    # Compute MSE
    mse = np.mean((true_theta - agent_theta)**2)
    threshold = 0.005

    assert mse <= threshold, f"MSE of theta is {mse:.6f}, which exceeds the threshold of {threshold}."