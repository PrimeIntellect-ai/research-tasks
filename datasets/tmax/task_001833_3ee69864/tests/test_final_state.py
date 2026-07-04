# test_final_state.py

import os
import numpy as np
import scipy.io.wavfile as wav
import pandas as pd
import pytest

def test_scaling_plan_mse():
    """Check the MSE of the RMS calculation and verify Replica counts."""
    output_file = '/home/user/scaling_plan.txt'
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    # Read ground truth audio
    wav_path = '/app/sonar_data.wav'
    assert os.path.exists(wav_path), f"Ground truth audio {wav_path} is missing."

    rate, data = wav.read(wav_path)
    chunk_size = 4410
    num_chunks = len(data) // chunk_size

    expected_rms = []
    expected_replicas = []
    for i in range(num_chunks):
        chunk = data[i*chunk_size : (i+1)*chunk_size].astype(np.float64)
        rms = np.sqrt(np.mean(chunk**2))
        expected_rms.append(rms)
        expected_replicas.append(max(1, int(rms / 500)))

    # Read agent's output
    try:
        agent_df = pd.read_csv(output_file, header=None, names=['Chunk', 'RMS', 'Replicas'])
    except Exception as e:
        pytest.fail(f"Could not read {output_file} as CSV: {e}")

    assert len(agent_df) >= num_chunks, f"Expected at least {num_chunks} rows in {output_file}, got {len(agent_df)}"

    agent_rms = agent_df['RMS'].values[:num_chunks]

    # Calculate MSE
    mse = np.mean((np.array(expected_rms) - agent_rms)**2)
    assert mse <= 0.1, f"MSE of RMS values is {mse}, which exceeds the threshold of 0.1."

    # Verify Replicas
    agent_replicas = agent_df['Replicas'].values[:num_chunks]
    replicas_match = np.array_equal(agent_replicas, expected_replicas)
    assert replicas_match, "Replica counts do not match the expected formula Replicas = max(1, integer_part(RMS / 500))."

def test_required_scripts_exist():
    """Check if the required bash scripts and C++ source exist."""
    assert os.path.exists("/home/user/start_api.sh"), "Missing /home/user/start_api.sh"
    assert os.path.exists("/home/user/operator.cpp"), "Missing /home/user/operator.cpp"
    assert os.path.exists("/home/user/deploy.sh"), "Missing /home/user/deploy.sh"
    assert os.path.exists("/home/user/operator_bin"), "Missing compiled binary /home/user/operator_bin"