# test_final_state.py

import os
import numpy as np
import pandas as pd
import imageio

def get_reference_data(video_path):
    """
    Computes the reference rolling variance of mean grayscale intensities
    from the video, mimicking OpenCV's BGR2GRAY conversion.
    """
    reader = imageio.get_reader(video_path)
    intensities = []
    for frame in reader:
        # imageio reads in RGB format.
        # OpenCV's COLOR_BGR2GRAY formula: Y = 0.299*R + 0.587*G + 0.114*B
        # We cast to uint8 to match cv2.cvtColor behavior.
        gray = (0.299 * frame[:, :, 0] + 0.587 * frame[:, :, 1] + 0.114 * frame[:, :, 2]).astype(np.uint8)
        intensities.append(gray.mean())

    df = pd.DataFrame({'frame_index': range(len(intensities)), 'intensity': intensities})
    df['rolling_variance'] = df['intensity'].rolling(window=5).var()
    df = df.dropna(subset=['rolling_variance'])
    return df

def test_rolling_variance_mse():
    results_path = "/home/user/results.csv"
    video_path = "/app/experiment_record.mp4"

    assert os.path.exists(results_path), f"Output file not found at {results_path}"
    assert os.path.exists(video_path), f"Video file not found at {video_path}"

    try:
        agent_df = pd.read_csv(results_path)
    except Exception as e:
        raise AssertionError(f"Failed to read {results_path} as CSV: {e}")

    assert 'frame_index' in agent_df.columns, "Column 'frame_index' is missing from results.csv"
    assert 'rolling_variance' in agent_df.columns, "Column 'rolling_variance' is missing from results.csv"

    agent_df = agent_df.sort_values('frame_index').reset_index(drop=True)

    # Compute reference data
    ref_df = get_reference_data(video_path)
    ref_df = ref_df.sort_values('frame_index').reset_index(drop=True)

    assert len(agent_df) == len(ref_df), (
        f"Row count mismatch. Expected {len(ref_df)} rows (excluding the first 4 NaN frames), "
        f"got {len(agent_df)}."
    )

    mse = np.mean((agent_df['rolling_variance'] - ref_df['rolling_variance']) ** 2)
    threshold = 0.01

    assert mse <= threshold, (
        f"Mean Squared Error of rolling_variance is too high. "
        f"Expected MSE <= {threshold}, but got {mse:.5f}."
    )