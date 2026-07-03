# test_final_state.py
import os
import json
import cv2
import pytest

def test_final_state():
    index_path = "/home/user/repository/index.json"
    assert os.path.exists(index_path), f"Index file is missing at {index_path}"

    with open(index_path, 'r') as f:
        try:
            index_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {index_path} is not valid JSON")

    predicted_frames = []
    for bundle, frames in index_data.items():
        assert isinstance(frames, list), f"Value for {bundle} in index.json must be a list of integers"
        predicted_frames.extend(frames)
    predicted_frames = set(predicted_frames)

    video_path = "/app/data_stream.mp4"
    assert os.path.exists(video_path), f"Video file is missing at {video_path}"

    cap = cv2.VideoCapture(video_path)
    true_frames = set()
    frame_idx = 1
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        avg_brightness = gray.mean()
        if avg_brightness > 128:
            true_frames.add(frame_idx)
        frame_idx += 1
    cap.release()

    tp = len(true_frames.intersection(predicted_frames))
    fp = len(predicted_frames - true_frames)
    fn = len(true_frames - predicted_frames)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    assert f1 >= 0.98, f"F1 score {f1:.4f} is below the threshold of 0.98. Precision: {precision:.4f}, Recall: {recall:.4f}"

    for bundle in index_data.keys():
        bundle_path = os.path.join("/home/user/repository", bundle)
        assert os.path.exists(bundle_path), f"Bundle {bundle_path} listed in index but missing on disk"