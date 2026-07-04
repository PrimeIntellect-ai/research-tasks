# test_final_state.py

import os
import re
import subprocess
from collections import deque
import pytest

def test_throughput_metric():
    """
    Run the verifier benchmark and ensure the throughput is >= 15000 edges/sec.
    """
    benchmark_script = "/app/verifier_benchmark.py"
    assert os.path.isfile(benchmark_script), f"Benchmark script missing at {benchmark_script}"

    try:
        result = subprocess.run(
            ["python3", benchmark_script],
            capture_output=True,
            text=True,
            timeout=30
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Benchmark script timed out. Deadlock might still be present.")

    assert result.returncode == 0, f"Benchmark script failed with error:\n{result.stderr}"

    # Extract throughput from stdout. The benchmark prints it.
    # We look for a number in the output.
    match = re.search(r"([\d\.]+)", result.stdout)
    assert match is not None, f"Could not parse throughput from benchmark output:\n{result.stdout}"

    throughput = float(match.group(1))
    threshold = 15000.0

    assert throughput >= threshold, (
        f"Throughput {throughput:.2f} edges/sec is below the required threshold of {threshold} edges/sec. "
        "Ensure you are using fine-grained locks and not a single global lock."
    )

def test_shortest_path_result():
    """
    Verify the shortest path written by the student in /home/user/shortest_path.txt.
    """
    csv_path = "/app/data/transactions.csv"
    assert os.path.isfile(csv_path), f"Data file missing at {csv_path}"

    # Recompute the shortest path to avoid hardcoding
    adj = {}
    with open(csv_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('source'):
                continue
            parts = line.split(',')
            if len(parts) >= 2:
                u, v = parts[0].strip(), parts[1].strip()
                adj.setdefault(u, set()).add(v)
                adj.setdefault(v, set()).add(u)

    start_node = 'CUST_739'
    end_node = 'CUST_882'

    # BFS to find the shortest path length
    queue = deque([[start_node]])
    visited = {start_node}
    expected_length = None

    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == end_node:
            expected_length = len(path)
            break
        for neighbor in sorted(adj.get(node, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    assert expected_length is not None, f"No path found between {start_node} and {end_node} in the dataset."

    student_file = "/home/user/shortest_path.txt"
    assert os.path.isfile(student_file), f"Student output file missing at {student_file}"

    with open(student_file, 'r') as f:
        student_content = f.read().strip()

    assert student_content, "Shortest path file is empty."

    student_path = [node.strip() for node in student_content.split(',')]

    assert student_path[0] == start_node, f"Path must start with {start_node}, got {student_path[0]}"
    assert student_path[-1] == end_node, f"Path must end with {end_node}, got {student_path[-1]}"
    assert len(student_path) == expected_length, (
        f"Expected shortest path length of {expected_length} nodes, "
        f"but got {len(student_path)} nodes."
    )

    # Verify that the path is valid in the graph
    for i in range(len(student_path) - 1):
        u = student_path[i]
        v = student_path[i+1]
        assert v in adj.get(u, set()), f"Invalid edge in path: {u} -> {v} does not exist in the graph."