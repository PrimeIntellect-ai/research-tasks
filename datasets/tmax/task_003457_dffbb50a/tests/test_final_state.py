# test_final_state.py

import os
import time
import subprocess
import pytest
from collections import defaultdict

def test_edges_csv_exists_and_format():
    csv_path = "/home/user/edges.csv"
    assert os.path.exists(csv_path), f"{csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0, f"{csv_path} is empty."

    for line in lines:
        parts = line.split(',')
        assert len(parts) == 2, f"Line '{line}' in {csv_path} does not have exactly two comma-separated values."
        try:
            int(parts[0].strip())
            int(parts[1].strip())
        except ValueError:
            pytest.fail(f"Line '{line}' in {csv_path} contains non-integer node IDs.")

def test_optimization_report_exists():
    report_path = "/home/user/optimization_report.txt"
    assert os.path.exists(report_path), f"Optimization report missing at {report_path}."
    assert os.path.getsize(report_path) > 0, f"Optimization report at {report_path} is empty."

def compute_expected_output(edges):
    adj = defaultdict(list)
    nodes = set()
    for u, v in edges:
        adj[u].append(v)
        nodes.add(u)
        nodes.add(v)

    path_counts = {}
    for a in nodes:
        count = 0
        for b in adj[a]:
            count += len(adj[b])
        path_counts[a] = count

    sorted_nodes = sorted(list(nodes))

    output_lines = []
    rolling_window = []
    for a in sorted_nodes:
        rolling_window.append(path_counts[a])
        if len(rolling_window) > 3:
            rolling_window.pop(0)
        rolling_sum = sum(rolling_window)
        output_lines.append(f"{a},{rolling_sum}")

    return "\n".join(output_lines)

def test_query_engine_performance_and_correctness():
    exe_path = "/home/user/query_engine_opt"
    assert os.path.exists(exe_path), f"Optimized executable missing at {exe_path}."
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable."

    csv_path = "edges.csv"

    # Generate a test dataset of 100,000 edges
    num_edges = 100000
    edges = []
    # Create a line graph with some branches
    for i in range(1, num_edges + 1):
        edges.append((i, i + 1))
        if i % 10 == 0:
            edges.append((i, i + 2))

    # Write to edges.csv in the directory where we will run the command
    run_dir = "/home/user"
    target_csv = os.path.join(run_dir, "edges.csv")

    # Backup original
    backup_csv = os.path.join(run_dir, "edges_backup.csv")
    if os.path.exists(target_csv):
        os.rename(target_csv, backup_csv)

    try:
        with open(target_csv, "w") as f:
            for u, v in edges:
                f.write(f"{u},{v}\n")

        expected_output = compute_expected_output(edges)

        start_time = time.time()
        result = subprocess.run([exe_path], cwd=run_dir, capture_output=True, text=True)
        end_time = time.time()

        execution_time = end_time - start_time

        assert result.returncode == 0, f"Executable failed with return code {result.returncode}. Stderr: {result.stderr}"

        # Check correctness
        actual_output = result.stdout.strip()

        # We compare a subset or the full string, but full string is exact
        # The output format should be matching
        # If the student used spaces, we can normalize
        def normalize(text):
            return "\n".join([line.replace(" ", "") for line in text.strip().split("\n") if line.strip()])

        assert normalize(actual_output) == normalize(expected_output), "The output of the optimized engine does not match the expected mathematical result."

        # Check metric threshold
        threshold = 0.15
        assert execution_time <= threshold, f"Execution time {execution_time:.4f}s exceeded the threshold of {threshold}s."

    finally:
        # Restore original
        if os.path.exists(backup_csv):
            os.replace(backup_csv, target_csv)
        elif os.path.exists(target_csv):
            os.remove(target_csv)