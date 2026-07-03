# test_final_state.py

import os
import time
import json
import subprocess
import pytest
import numpy as np
import imageio

def test_video_events():
    video_path = "/app/traffic_video.mp4"
    events_path = "/home/user/video_events.jsonl"

    assert os.path.exists(events_path), f"Missing expected output file: {events_path}"
    assert os.path.exists(video_path), f"Missing video file: {video_path}"

    # Recompute expected events
    reader = imageio.get_reader(video_path)
    frames = []
    for frame in reader:
        frames.append(frame)

    expected_events = []
    for i in range(0, len(frames), 30):
        segment = frames[i:i+30]
        if len(segment) < 2:
            continue

        diffs = []
        for j in range(1, len(segment)):
            diff = np.abs(segment[j].astype(np.float32) - segment[j-1].astype(np.float32))
            diffs.append(np.mean(diff))

        avg_diff = np.mean(diffs)
        if avg_diff > 5.0:
            expected_events.append({"segment_index": i // 30, "status": "high_traffic"})

    # Read actual events
    actual_events = []
    with open(events_path, "r") as f:
        for line in f:
            if line.strip():
                try:
                    actual_events.append(json.loads(line))
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON line in {events_path}: {line}")

    assert len(actual_events) == len(expected_events), f"Expected {len(expected_events)} events, found {len(actual_events)}"
    for actual, expected in zip(actual_events, expected_events):
        assert actual == expected, f"Mismatch in video events. Expected {expected}, got {actual}"

def test_query_pipeline_speedup():
    original_path = "/app/hidden/query_pipeline_original.py"
    optimized_path = "/home/user/query_pipeline_optimized.py"

    assert os.path.exists(optimized_path), f"Missing optimized script: {optimized_path}"
    assert os.path.exists(original_path), f"Missing original script backup: {original_path}"

    # Run original
    start_orig = time.time()
    res_orig = subprocess.run(["python3", original_path], capture_output=True, text=True, check=True)
    time_orig = time.time() - start_orig

    # Run optimized
    start_opt = time.time()
    res_opt = subprocess.run(["python3", optimized_path], capture_output=True, text=True)
    time_opt = time.time() - start_opt

    assert res_opt.returncode == 0, f"Optimized script failed with error:\n{res_opt.stderr}"

    # Parse outputs
    try:
        out_orig = json.loads(res_orig.stdout)
    except json.JSONDecodeError:
        pytest.fail("Original script did not output valid JSON. Environment might be corrupted.")

    try:
        out_opt = json.loads(res_opt.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Optimized script did not output valid JSON. Output was:\n{res_opt.stdout}")

    # Verify correctness
    assert set(out_orig.keys()) == set(out_opt.keys()), "Optimized output nodes do not match original."
    for k in out_orig:
        assert abs(out_orig[k] - out_opt[k]) < 1e-4, f"Mismatch in centrality for node {k}. Expected {out_orig[k]}, got {out_opt[k]}"

    # Verify speedup
    speedup = time_orig / time_opt
    assert speedup >= 3.0, f"Speedup {speedup:.2f} is less than required 3.0 (Original: {time_orig:.2f}s, Optimized: {time_opt:.2f}s)"