# test_final_state.py

import os
import pytest
import pandas as pd
import numpy as np

def test_libminifft_built():
    lib_file = "/app/minifft-1.2.0/libminifft.a"
    assert os.path.isfile(lib_file), f"Expected static library {lib_file} was not built."

def test_pipeline_script_exists():
    script_path = "/home/user/workspace/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script {script_path} does not exist."

def test_cpp_source_exists():
    cpp_path = "/home/user/workspace/wave_sim.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} does not exist."

def test_spectrum_mse():
    csv_path = "/home/user/workspace/spectrum.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist. Did the pipeline run?"

    # Ground truth generation
    N = 1024
    t = np.linspace(0, 1, N, endpoint=False)
    y = np.sin(2 * np.pi * 10 * t) + 0.5 * np.cos(2 * np.pi * 25 * t)
    fft_gt = np.abs(np.fft.fft(y))[:50]

    # Load agent's output
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        pytest.fail(f"Failed to read {csv_path} as CSV: {e}")

    assert 'magnitude' in df.columns, "The CSV file must contain a 'magnitude' column."

    agent_mag = df['magnitude'].values
    assert len(agent_mag) >= 50, f"Expected at least 50 bins in the output, but got {len(agent_mag)}."

    agent_mag = agent_mag[:50]

    mse = np.mean((fft_gt - agent_mag)**2)
    threshold = 1e-4

    assert mse < threshold, f"MSE of magnitudes is {mse}, which is not below the threshold of {threshold}."