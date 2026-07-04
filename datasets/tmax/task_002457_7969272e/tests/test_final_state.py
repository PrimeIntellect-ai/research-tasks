# test_final_state.py

import os
import sys
import numpy as np
from scipy.io import wavfile
from scipy.stats import wasserstein_distance

def compute_reference():
    sample_rate, data = wavfile.read('/app/signal.wav')
    if len(data.shape) > 1:
        data = data[:, 0]
    normalized_data = data.astype(np.float32) / 32768.0
    np.random.seed(42)
    ideal_samples = np.random.normal(0, 0.1, len(normalized_data))
    return wasserstein_distance(normalized_data, ideal_samples)

def test_c_source_exists():
    """Test that the C source file was created."""
    assert os.path.isfile('/home/user/src/wav_extract.c'), "C source file /home/user/src/wav_extract.c is missing."

def test_executable_exists():
    """Test that the C program was compiled to the correct location."""
    assert os.path.isfile('/home/user/bin/wav_extract'), "Executable /home/user/bin/wav_extract is missing."
    assert os.access('/home/user/bin/wav_extract', os.X_OK), "/home/user/bin/wav_extract is not executable."

def test_bash_script_exists():
    """Test that the bash script was created."""
    assert os.path.isfile('/home/user/analyze_noise.sh'), "Bash script /home/user/analyze_noise.sh is missing."
    assert os.access('/home/user/analyze_noise.sh', os.X_OK), "/home/user/analyze_noise.sh is not executable."

def test_distance_output():
    """Test that the final distance.txt contains the correct Wasserstein distance."""
    output_file = '/home/user/distance.txt'
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    with open(output_file, 'r') as f:
        content = f.read().strip()

    try:
        agent_val = float(content)
    except ValueError:
        assert False, f"Content of {output_file} is not a valid float: '{content}'"

    ref_val = compute_reference()
    error = abs(agent_val - ref_val)

    assert error <= 0.01, f"Predicted distance {agent_val} differs from reference {ref_val} by {error}, which is > 0.01 threshold."