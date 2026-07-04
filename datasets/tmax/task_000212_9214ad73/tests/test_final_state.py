# test_final_state.py
import os
import cv2
import sqlite3
import heapq
import pytest

def get_reference_value():
    """
    Re-derives the ground truth shortest path by analyzing the video
    and database exactly as specified in the rubric.
    """
    video_path = '/app/network_traffic.mp4'
    assert os.path.isfile(video_path), "Video file missing, cannot compute reference."

    cap = cv2.VideoCapture(video_path)
    fps = 30.0
    flash_timestamps = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Check if top-left 50x50 is pure white
        roi = frame[0:50, 0:50]
        if (roi == 255).all():
            flash_timestamps.append(frame_idx / fps)
        frame_idx += 1
    cap.release()

    db_path = '/app/network.db'
    assert os.path.isfile(db_path), "Database file missing, cannot compute reference."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Read all rows to bypass any potential index corruption
    c.execute("SELECT event_time, source_node, target_node, payload_size FROM event_logs")
    rows = c.fetchall()
    conn.close()

    # Filter rows based on timestamps
    edges = []
    for row in rows:
        event_time, src, dst, weight = row
        for ts in flash_timestamps:
            if abs(event_time - ts) <= 0.1:
                edges.append((src, dst, weight))
                break

    # Compute shortest path from NODE_A to NODE_Z using Dijkstra's algorithm
    graph = {}
    for src, dst, weight in edges:
        if src not in graph:
            graph[src] = []
        graph[src].append((dst, weight))

    pq = [(0, 'NODE_A')]
    visited = set()
    shortest_path = float('inf')

    while pq:
        cost, node = heapq.heappop(pq)
        if node == 'NODE_Z':
            shortest_path = cost
            break
        if node in visited:
            continue
        visited.add(node)
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor))

    return shortest_path

def test_result_metric():
    result_path = '/home/user/result.txt'
    assert os.path.isfile(result_path), f"Expected result file at {result_path} is missing."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {result_path} ('{content}') as a float.")

    reference = get_reference_value()
    assert reference != float('inf'), "Reference calculation failed to find a path."

    error = abs(val - reference) / reference
    assert error <= 0.01, (
        f"Metric failed: absolute percentage error {error:.4f} is greater than threshold 0.01. "
        f"Expected a value close to {reference}, but got {val}."
    )