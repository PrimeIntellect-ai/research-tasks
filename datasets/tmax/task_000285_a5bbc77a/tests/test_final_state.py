# test_final_state.py

import os
import socket
import csv
import pytest
from collections import defaultdict

def test_hierarchy_csv_exists_and_valid():
    """Check that hierarchy.csv exists and has exactly two integer columns."""
    hierarchy_path = "/home/user/hierarchy.csv"
    assert os.path.exists(hierarchy_path), f"File {hierarchy_path} does not exist."

    with open(hierarchy_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            assert len(row) == 2, f"Expected exactly 2 columns in hierarchy.csv, got {len(row)}: {row}"
            try:
                int(row[0])
                int(row[1])
            except ValueError:
                pytest.fail(f"Values in hierarchy.csv must be integers, got: {row}")

def test_server_reports():
    """Check that the server on port 8888 returns the correct transitive descendants."""
    hierarchy_path = "/home/user/hierarchy.csv"
    assert os.path.exists(hierarchy_path), f"File {hierarchy_path} does not exist."

    # Build the expected graph from the generated hierarchy.csv
    graph = defaultdict(list)
    nodes = set()
    with open(hierarchy_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 2:
                continue
            try:
                mgr, emp = int(row[0]), int(row[1])
                graph[mgr].append(emp)
                nodes.add(mgr)
                nodes.add(emp)
            except ValueError:
                pass

    def get_all_descendants(node):
        desc = set()
        stack = [node]
        while stack:
            curr = stack.pop()
            for child in graph[curr]:
                if child not in desc:
                    desc.add(child)
                    stack.append(child)
        return desc

    # Pick a few nodes to test: the root (if identifiable) and some others
    test_nodes = list(nodes)[:10]

    for node in test_nodes:
        expected = get_all_descendants(node)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.0)
            try:
                s.connect(('127.0.0.1', 8888))
            except ConnectionRefusedError:
                pytest.fail("Server is not listening on 127.0.0.1:8888")

            s.sendall(f"REPORTS {node}\n".encode('utf-8'))

            data = b""
            while b"\n" not in data:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk

            response = data.decode('utf-8').strip()

            if not expected:
                assert response == "", f"Expected empty response for node {node} (no descendants), got '{response}'"
            else:
                assert response != "", f"Expected descendants for node {node}, got empty response"
                try:
                    actual_desc = set(map(int, response.split(',')))
                except ValueError:
                    pytest.fail(f"Server returned invalid format for node {node}: '{response}'")

                assert actual_desc == expected, f"Descendants mismatch for node {node}. Expected {expected}, got {actual_desc}"