# test_final_state.py
import os
import pandas as pd
import numpy as np
import pytest

def test_final_results():
    output_path = "/home/user/ci_results.csv"
    assert os.path.isfile(output_path), f"Output file not found at {output_path}"

    data_path = "/home/user/rna_data.csv"
    assert os.path.isfile(data_path), f"Input data file missing at {data_path}"

    df = pd.read_csv(data_path)
    k_base, k_A, k_U, k_G, k_C = 0.010, 0.025, 0.015, 0.030, 0.040

    def rk4_final(seq):
        length = len(seq)
        k = k_base + (seq.count('A')*k_A + seq.count('U')*k_U + seq.count('G')*k_G + seq.count('C')*k_C) / length

        C = 100.0
        dt = 0.1
        for _ in range(200):
            k1 = -k * C - 0.002 * C**2

            C_half1 = C + 0.5 * dt * k1
            k2 = -k * C_half1 - 0.002 * C_half1**2

            C_half2 = C + 0.5 * dt * k2
            k3 = -k * C_half2 - 0.002 * C_half2**2

            C_full = C + dt * k3
            k4 = -k * C_full - 0.002 * C_full**2

            C += (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        return C

    final_concs = np.array([rk4_final(seq) for seq in df['Sequence']])
    true_mean = np.mean(final_concs)
    std_err = np.std(final_concs, ddof=1) / np.sqrt(len(final_concs))

    # For 95% CI, normal approximation is fine since N=5000
    true_lower = true_mean - 1.96 * std_err
    true_upper = true_mean + 1.96 * std_err

    try:
        agent_df = pd.read_csv(output_path)
        agent_mean = float(agent_df['Mean'].iloc[0])
        agent_lower = float(agent_df['Lower95'].iloc[0])
        agent_upper = float(agent_df['Upper95'].iloc[0])
    except Exception as e:
        pytest.fail(f"Failed to read or parse {output_path}. Ensure it has columns Mean, Lower95, Upper95. Error: {e}")

    err_mean = abs(agent_mean - true_mean)
    err_lower = abs(agent_lower - true_lower)
    err_upper = abs(agent_upper - true_upper)

    max_err = max(err_mean, err_lower, err_upper)

    threshold = 0.2
    assert max_err <= threshold, (
        f"Maximum absolute error {max_err:.4f} exceeds threshold {threshold}. "
        f"True Mean: {true_mean:.4f}, Agent Mean: {agent_mean:.4f} | "
        f"True Lower95: {true_lower:.4f}, Agent Lower95: {agent_lower:.4f} | "
        f"True Upper95: {true_upper:.4f}, Agent Upper95: {agent_upper:.4f}"
    )