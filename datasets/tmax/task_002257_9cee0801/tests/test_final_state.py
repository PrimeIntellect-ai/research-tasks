# test_final_state.py
import os
import subprocess
import numpy as np
import pandas as pd

def generate_ground_truth():
    cmd = [
        "ffmpeg", "-i", "/app/video.mp4", "-vf", "signalstats",
        "-f", "null", "-"
    ]
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)

    data = []
    for line in process.stderr:
        if "Parsed_signalstats_" in line and "YAVG" in line:
            parts = line.split()
            yavg = None
            savg = None
            for p in parts:
                if p.startswith("YAVG:"):
                    yavg = float(p.split(":")[1])
                if p.startswith("SAVG:"):
                    savg = float(p.split(":")[1])
            if yavg is not None and savg is not None:
                data.append({'YAVG': yavg, 'SAVG': savg})

    df = pd.DataFrame(data)
    df['frame_num'] = np.arange(1, len(df) + 1)

    W_Y = 0.15
    W_S = -0.08
    B = -12.5

    df['Z'] = W_Y * df['YAVG'] + W_S * df['SAVG'] + B
    df['probability'] = 1 / (1 + np.exp(-df['Z']))
    return df[['frame_num', 'probability']]

def test_predictions_mse():
    predictions_path = "/home/user/predictions.csv"
    assert os.path.exists(predictions_path), f"Predictions file not found at {predictions_path}"

    try:
        agent_df = pd.read_csv(predictions_path)
    except Exception as e:
        assert False, f"Failed to read {predictions_path} as CSV: {e}"

    assert 'frame_num' in agent_df.columns, "Column 'frame_num' is missing from predictions.csv"
    assert 'probability' in agent_df.columns, "Column 'probability' is missing from predictions.csv"

    gt_df = generate_ground_truth()

    merged = pd.merge(gt_df, agent_df, on="frame_num", suffixes=('_gt', '_agent'))
    assert len(merged) > 0, "No overlapping frames found between ground truth and predictions"

    mse = np.mean((merged['probability_gt'] - merged['probability_agent'])**2)

    assert mse <= 0.0001, f"MSE is {mse:.6f}, which is greater than the threshold of 0.0001"