# test_final_state.py

import os
import cv2
import pandas as pd
import numpy as np
import pytest

def get_ground_truth_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    records = []
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Calculate average color channels
        # OpenCV uses BGR
        b = int(round(np.mean(frame[:, :, 0])))
        g = int(round(np.mean(frame[:, :, 1])))
        r = int(round(np.mean(frame[:, :, 2])))

        # R channel represents node_id. Ignore if 0.
        if r != 0:
            records.append({'frame_idx': frame_idx, 'node_id': r, 'parent_id': g, 'value': b})
        frame_idx += 1
    cap.release()

    df = pd.DataFrame(records)
    if df.empty:
        return df

    # Build parent map to calculate depth
    parent_map = {}
    for _, row in df.iterrows():
        parent_map[row['node_id']] = row['parent_id']

    def get_depth(node):
        depth = 0
        curr = node
        visited = set()
        while curr in parent_map and parent_map[curr] != 0:
            if curr in visited:
                break # Prevent infinite loops if data is corrupted
            visited.add(curr)
            depth += 1
            curr = parent_map[curr]
        return depth

    df['depth'] = df['node_id'].apply(get_depth)
    # Path-Smoothed Value = The current reading's value + the count of its ancestors
    df['path_smoothed_value'] = df['value'] + df['depth']

    # Moving Average: 3-frame rolling average of Path-Smoothed Value for each node_id, ordered by frame_idx
    df = df.sort_values(['node_id', 'frame_idx'])
    df['rolling_avg'] = df.groupby('node_id')['path_smoothed_value'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())

    # Return to original order
    df = df.sort_values('frame_idx').reset_index(drop=True)
    return df[['frame_idx', 'node_id', 'rolling_avg']]

def test_results_exist():
    results_path = '/home/user/results.csv'
    assert os.path.exists(results_path), f"The results file {results_path} is missing."

def test_rolling_avg_mse():
    results_path = '/home/user/results.csv'
    video_path = '/app/sensor_feed.mp4'
    gt_path = '/tmp/ground_truth.csv'

    assert os.path.exists(results_path), f"Results file {results_path} not found."

    # Load ground truth
    if os.path.exists(gt_path):
        gt = pd.read_csv(gt_path)
    else:
        assert os.path.exists(video_path), f"Video file {video_path} not found to derive ground truth."
        gt = get_ground_truth_from_video(video_path)

    assert not gt.empty, "Ground truth data is empty."

    # Load agent results
    try:
        agent = pd.read_csv(results_path)
    except Exception as e:
        pytest.fail(f"Failed to read {results_path}: {e}")

    assert 'frame_idx' in agent.columns, "Column 'frame_idx' missing in results.csv"
    assert 'node_id' in agent.columns, "Column 'node_id' missing in results.csv"
    assert 'rolling_avg' in agent.columns, "Column 'rolling_avg' missing in results.csv"

    # Merge on frame_idx and node_id
    merged = pd.merge(gt, agent, on=['frame_idx', 'node_id'], suffixes=('_gt', '_agent'))

    assert len(merged) > 0, "No matching frames between ground truth and agent results."
    assert len(merged) == len(gt), f"Agent results are missing rows. Expected {len(gt)}, got {len(merged)} matching rows."

    # Calculate MSE
    mse = np.mean((merged['rolling_avg_gt'] - merged['rolling_avg_agent'])**2)

    # Pass condition
    assert mse <= 0.05, f"MSE {mse:.4f} exceeds threshold 0.05"