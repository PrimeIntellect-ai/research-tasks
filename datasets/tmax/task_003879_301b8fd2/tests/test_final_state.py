# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_bootstrap_mean_accuracy():
    """
    Recomputes the true sample mean of the predictions and compares it
    to the agent's bootstrap mean in /home/user/final_result.txt.
    """
    final_result_path = "/home/user/final_result.txt"
    assert os.path.exists(final_result_path), f"Missing required file: {final_result_path}"

    # Read agent's prediction
    try:
        with open(final_result_path, "r") as f:
            agent_val = float(f.read().strip())
    except Exception as e:
        pytest.fail(f"Could not read a valid numeric value from {final_result_path}. Error: {e}")

    # Read weights from /app/weights.csv
    weights_path = "/app/weights.csv"
    assert os.path.exists(weights_path), f"Missing weights file: {weights_path}"
    with open(weights_path, "r") as wf:
        weights_str = wf.read().strip()
        intercept, w_max, w_mean = map(float, weights_str.split(","))

    # Recompute truth
    os.makedirs("/tmp/truth_segments", exist_ok=True)
    subprocess.run(
        "ffmpeg -y -i /app/recording.wav -f segment -segment_time 1 -c copy /tmp/truth_segments/out%03d.wav",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    preds = []
    for f in sorted(glob.glob("/tmp/truth_segments/out*.wav")):
        res = subprocess.run(
            f"ffmpeg -i {f} -af volumedetect -f null /dev/null 2>&1",
            shell=True,
            capture_output=True,
            text=True
        )
        max_v, mean_v = None, None
        for line in res.stderr.splitlines():
            if "max_volume:" in line:
                max_v = float(line.split("max_volume:")[1].replace("dB", "").strip())
            if "mean_volume:" in line:
                mean_v = float(line.split("mean_volume:")[1].replace("dB", "").strip())

        if max_v is not None and mean_v is not None:
            pred = intercept + (w_max * max_v) + (w_mean * mean_v)
            preds.append(pred)

    assert len(preds) > 0, "Failed to compute truth: no valid segments found in /app/recording.wav"

    true_mean = sum(preds) / len(preds)
    error = abs(true_mean - agent_val)
    threshold = 0.5

    assert error <= threshold, (
        f"Bootstrap estimate error is too high! "
        f"True sample mean: {true_mean:.4f}, Agent's value: {agent_val:.4f}. "
        f"Absolute error: {error:.4f} (Threshold: <= {threshold})"
    )