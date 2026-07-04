# test_final_state.py
import os
import sys
import json
import pytest

def test_adversarial_corpus():
    sys.path.insert(0, '/home/user')
    try:
        from validator import is_safe_expression
    except ImportError:
        pytest.fail("Could not import is_safe_expression from /home/user/validator.py")

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = sorted([f for f in os.listdir(clean_dir) if f.endswith('.txt')])
    evil_files = sorted([f for f in os.listdir(evil_dir) if f.endswith('.txt')])

    clean_failed = []
    for cf in clean_files:
        with open(os.path.join(clean_dir, cf), 'r') as f:
            expr = f.read().strip()
        try:
            if not is_safe_expression(expr):
                clean_failed.append(cf)
        except Exception:
            clean_failed.append(cf)

    evil_failed = []
    for ef in evil_files:
        with open(os.path.join(evil_dir, ef), 'r') as f:
            expr = f.read().strip()
        try:
            if is_safe_expression(expr):
                evil_failed.append(ef)
        except Exception:
            pass  # Exception means it's rejected, which is expected for evil corpus

    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_result_json():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"File {result_path} not found"

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{result_path} is not valid JSON")

    assert isinstance(data, list), "Result must be a JSON array"
    assert all(isinstance(x, int) for x in data), "Result array must contain only integers"

    import cv2
    video_path = "/app/sample_video.mp4"
    cap = cv2.VideoCapture(video_path)
    assert cap.isOpened(), f"Could not open {video_path}"

    frame_index = 0
    expected_indices = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # cv2.mean returns (B, G, R, A)
        b_mean, g_mean, r_mean = cv2.mean(frame)[:3]
        if r_mean > g_mean + 20 and frame_index > 50:
            expected_indices.append(frame_index)
        frame_index += 1
    cap.release()

    assert data == expected_indices, f"Result indices do not match ground truth. Expected {expected_indices}, got {data}"