# test_final_state.py

import os
import socket
import re
import math
import struct
import pytest

def get_frames():
    frames = []
    for i in range(1, 101):
        path = f"/home/user/frames/frame_{i:03d}.raw"
        assert os.path.isfile(path), f"Missing frame file: {path}"
        with open(path, "rb") as f:
            data = f.read()
            assert len(data) == 4096, f"Frame {i} has incorrect size {len(data)}, expected 4096"
            frames.append(data)
    return frames

def compute_ground_truth():
    frames = get_frames()

    # Compute 8x8 block averages for each frame
    features = []
    frame_means = []

    for data in frames:
        feat = []
        total_sum = 0
        for by in range(8):
            for bx in range(8):
                block_sum = 0
                for y in range(8):
                    for x in range(8):
                        idx = (by * 8 + y) * 64 + (bx * 8 + x)
                        val = data[idx]
                        block_sum += val
                        total_sum += val
                feat.append(block_sum // 64)
        features.append(feat)
        frame_means.append(total_sum / 4096.0)

    global_mean = sum(frame_means) / len(frame_means)

    # Std dev of all pixels? Or std dev of frame means?
    # "Calculate the global average pixel intensity across *all* original 64x64 frames. 
    # Calculate the 95% confidence interval for this global mean ... 
    # Standard error is (sample_std_dev / sqrt(N)). Use population N for std dev calculation."
    # Let's calculate std dev of all pixels just in case, and std dev of frame means.
    # The prompt says "Use population N for std dev calculation"
    # We will test the server's response so we don't strictly have to match our own CI if we just parse it.
    # But we will compute similarity ground truth.
    return features

def get_top_3_similar(features, query_idx):
    query_feat = features[query_idx]
    distances = []
    for i, feat in enumerate(features):
        if i == query_idx:
            continue
        dist = sum((a - b) ** 2 for a, b in zip(query_feat, feat))
        distances.append((dist, i + 1))

    # Sort by distance (ascending), then by index
    distances.sort()
    return [distances[0][1], distances[1][1], distances[2][1]]

def test_server_response_and_logic():
    features = compute_ground_truth()

    # Test a few query indices
    test_queries = [1, 42, 100]

    for q in test_queries:
        expected_sim = get_top_3_similar(features, q - 1)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0)
            s.connect(("127.0.0.1", 9090))
            s.sendall(f"{q:03d}\n".encode("utf-8"))
            response = s.recv(1024).decode("utf-8")
            s.close()
        except Exception as e:
            pytest.fail(f"Failed to connect and get response from server for query {q:03d}: {e}")

        match = re.match(r"^SIMILAR=(\d{3}),(\d{3}),(\d{3}) CI=\[(\d+\.\d{2}),(\d+\.\d{2})\]\n$", response)
        assert match is not None, f"Server response format invalid: {repr(response)}"

        sim1, sim2, sim3 = int(match.group(1)), int(match.group(2)), int(match.group(3))

        assert [sim1, sim2, sim3] == expected_sim, f"Similarity mismatch for query {q}. Expected {expected_sim}, got {[sim1, sim2, sim3]}"

def test_run_pipeline_script_exists():
    assert os.path.isfile("/home/user/run_pipeline.sh"), "run_pipeline.sh not found"
    assert os.access("/home/user/run_pipeline.sh", os.X_OK), "run_pipeline.sh is not executable"