# test_final_state.py

import os
import csv
import math

def test_processed_logs_exists():
    """Verify that the processed_logs.csv file exists."""
    file_path = '/home/user/processed_logs.csv'
    assert os.path.exists(file_path), f"Output file is missing: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a file: {file_path}"

def test_processed_logs_contents():
    """Verify the contents of processed_logs.csv match the expected aggregated values."""
    file_path = '/home/user/processed_logs.csv'
    assert os.path.exists(file_path), f"Output file is missing: {file_path}"

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert reader.fieldnames == ['user_ip', 'cpu_usage', 'memory_usage'], \
        f"Incorrect columns. Expected ['user_ip', 'cpu_usage', 'memory_usage'], got {reader.fieldnames}"

    expected_data = {
        '10.0.0.0': {'cpu_usage': 38.33, 'memory_usage': 884.0},
        '10.1.1.0': {'cpu_usage': 50.0, 'memory_usage': 1072.0},
        '172.16.0.0': {'cpu_usage': 27.5, 'memory_usage': 578.0},
        '192.168.1.0': {'cpu_usage': 42.5, 'memory_usage': 868.0}
    }

    # Check sorting
    user_ips = [row['user_ip'] for row in rows]
    assert user_ips == sorted(user_ips), "The CSV is not sorted alphabetically by user_ip"

    assert len(rows) == len(expected_data), f"Expected {len(expected_data)} rows, got {len(rows)}"

    for row in rows:
        ip = row['user_ip']
        assert ip in expected_data, f"Unexpected user_ip found: {ip}"

        expected_cpu = expected_data[ip]['cpu_usage']
        expected_mem = expected_data[ip]['memory_usage']

        actual_cpu = float(row['cpu_usage'])
        actual_mem = float(row['memory_usage'])

        assert math.isclose(actual_cpu, expected_cpu, rel_tol=1e-4), \
            f"For IP {ip}, expected cpu_usage {expected_cpu}, got {actual_cpu}"
        assert math.isclose(actual_mem, expected_mem, rel_tol=1e-4), \
            f"For IP {ip}, expected memory_usage {expected_mem}, got {actual_mem}"

def test_pipeline_log_exists():
    """Verify that the pipeline.log file exists."""
    file_path = '/home/user/pipeline.log'
    assert os.path.exists(file_path), f"Log file is missing: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a file: {file_path}"

def test_pipeline_log_contents_and_order():
    """Verify the pipeline.log contains correct node executions in valid topological order."""
    file_path = '/home/user/pipeline.log'
    assert os.path.exists(file_path), f"Log file is missing: {file_path}"

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    events = []
    for line in lines:
        if line.startswith("[INFO] - Node ") and (" started." in line or " completed." in line):
            parts = line.split(" ")
            node_name = parts[3]
            action = parts[4].replace(".", "")
            events.append({"node": node_name, "action": action})

    required_nodes = {
        "Extract_Telemetry", "Extract_Access", "Impute_Telemetry",
        "Mask_Access", "Merge_And_Aggregate", "Load"
    }

    completed_nodes = set()
    started_nodes = set()

    # Track completion order
    completion_order = []

    for event in events:
        node = event["node"]
        action = event["action"]

        if action == "started":
            started_nodes.add(node)
            # Check dependencies before starting
            if node == "Impute_Telemetry":
                assert "Extract_Telemetry" in completed_nodes, "Impute_Telemetry started before Extract_Telemetry completed"
            elif node == "Mask_Access":
                assert "Extract_Access" in completed_nodes, "Mask_Access started before Extract_Access completed"
            elif node == "Merge_And_Aggregate":
                assert "Impute_Telemetry" in completed_nodes, "Merge_And_Aggregate started before Impute_Telemetry completed"
                assert "Mask_Access" in completed_nodes, "Merge_And_Aggregate started before Mask_Access completed"
            elif node == "Load":
                assert "Merge_And_Aggregate" in completed_nodes, "Load started before Merge_And_Aggregate completed"

        elif action == "completed":
            assert node in started_nodes, f"Node {node} completed before starting"
            completed_nodes.add(node)
            completion_order.append(node)

    for node in required_nodes:
        assert node in started_nodes, f"Node {node} never started"
        assert node in completed_nodes, f"Node {node} never completed"

    assert completion_order[-1] == "Load", "Load was not the last node to complete"