# test_final_state.py

import os
import sys
import subprocess
import pytest

def get_true_levels(audio_path):
    cmd = f"ffmpeg -i {audio_path} -af astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level -f null - 2>&1 | awk -F'=' '/RMS_level/ {{print $2}}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    levels = []
    for line in result.stdout.strip().split('\n'):
        if not line: continue
        val = line.strip()
        if val == '-inf':
            levels.append(-100.0)
        else:
            levels.append(float(val))
    return levels

def calc_sma(levels, window=5):
    sma = []
    for i in range(len(levels)):
        start = max(0, i - window + 1)
        sub = levels[start:i+1]
        sma.append(sum(sub) / len(sub))
    return sma

def test_smoothed_levels_mae():
    agent_file = "/home/user/smoothed_levels.txt"
    audio_file = "/app/alert_log.wav"

    assert os.path.exists(agent_file), f"Agent output file missing at {agent_file}"
    assert os.path.exists(audio_file), f"Audio fixture missing at {audio_file}"

    try:
        with open(agent_file, 'r') as f:
            agent_vals = [float(line.strip()) for line in f.readlines() if line.strip()]
    except Exception as e:
        pytest.fail(f"Failed to read or parse agent output from {agent_file}: {e}")

    true_levels = get_true_levels(audio_file)
    true_sma = calc_sma(true_levels)

    assert len(agent_vals) == len(true_sma), f"Length mismatch: Agent has {len(agent_vals)} values, expected {len(true_sma)} values."

    errors = [abs(a - t) for a, t in zip(agent_vals, true_sma)]
    mae = sum(errors) / len(errors)

    threshold = 0.05
    assert mae <= threshold, f"MAE exceeds threshold: {mae} > {threshold}. Agent values differ too much from the true SMA."