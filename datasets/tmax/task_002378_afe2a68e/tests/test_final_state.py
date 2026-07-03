# test_final_state.py

import os
import time
import subprocess
import wave
import numpy as np
import pytest

def test_optimized_monitor_exists():
    assert os.path.isfile("/home/user/optimized_monitor.sh"), "The script /home/user/optimized_monitor.sh does not exist."

def test_optimized_monitor_accuracy_and_performance():
    audio_file = '/app/stream.wav'
    assert os.path.isfile(audio_file), f"{audio_file} is missing."

    # Compute ground truth
    with wave.open(audio_file, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16)
        expected_energy = np.sum(samples.astype(np.float64) ** 2)

    # Run agent script
    script_path = '/home/user/optimized_monitor.sh'
    start = time.time()
    result = subprocess.run(['bash', script_path], capture_output=True, text=True)
    duration = time.time() - start

    assert result.returncode == 0, f"Script execution failed with error:\n{result.stderr}"

    try:
        agent_energy = float(result.stdout.strip())
    except ValueError:
        pytest.fail(f"Script output could not be parsed as a float. Output was: {result.stdout.strip()}")

    # Check accuracy
    error = abs(agent_energy - expected_energy) / expected_energy if expected_energy != 0 else abs(agent_energy)
    assert error < 0.01, f"Energy calculation is incorrect. Expected ~{expected_energy}, got {agent_energy}"

    # Check metric threshold
    assert duration <= 0.5, f"Execution time {duration:.3f}s exceeded threshold of 0.5s"