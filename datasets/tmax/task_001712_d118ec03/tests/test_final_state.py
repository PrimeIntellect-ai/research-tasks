# test_final_state.py

import os
import sqlite3
import pytest
import imageio.v3 as iio
from collections import defaultdict

def get_active_frames(video_path):
    active_frames = []
    frames = iio.imread(video_path, plugin="pyav")
    for i, frame in enumerate(frames):
        if frame.ndim == 3:
            gray = frame.mean(axis=2)
        else:
            gray = frame
        if gray.mean() > 100.0:
            active_frames.append(i)
    return set(active_frames)

def get_edges(db_path, active_frames):
    if not active_frames:
        return []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    placeholders = ','.join('?' for _ in active_frames)
    query = f"SELECT source, target FROM edges WHERE source IN ({placeholders}) AND target IN ({placeholders})"
    c.execute(query, tuple(active_frames) * 2)
    edges = c.fetchall()
    conn.close()
    return edges

def compute_avg_clustering(edges, active_frames):
    adj = defaultdict(set)
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)

    ccs = []
    for node in active_frames:
        neighbors = list(adj[node])
        k = len(neighbors)
        if k >= 2:
            links = 0
            for i in range(k):
                for j in range(i+1, k):
                    if neighbors[j] in adj[neighbors[i]]:
                        links += 1
            cc = links / (k * (k - 1) / 2.0)
            ccs.append(cc)

    if not ccs:
        return 0.0
    return sum(ccs) / len(ccs)

def test_result_accuracy():
    result_path = '/home/user/result.txt'
    assert os.path.isfile(result_path), f"Result file missing at {result_path}"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {result_path} as a float. Content: '{content}'")

    video_path = '/app/experiment.mp4'
    db_path = '/app/graph.db'

    assert os.path.isfile(video_path), f"Video file missing at {video_path}"
    assert os.path.isfile(db_path), f"Database file missing at {db_path}"

    active_frames = get_active_frames(video_path)
    edges = get_edges(db_path, active_frames)
    expected = compute_avg_clustering(edges, active_frames)

    diff = abs(val - expected)
    assert diff <= 0.005, f"Metric failed: Absolute difference between agent output ({val}) and expected ({expected}) is {diff}, which is > 0.005"