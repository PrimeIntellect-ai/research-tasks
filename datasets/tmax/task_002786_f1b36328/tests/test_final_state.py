# test_final_state.py

import os
import json
import csv
from collections import defaultdict

def test_max_2hop_csv_exists_and_correct():
    logs_file = "/home/user/data/logs.jsonl"
    output_file = "/home/user/data/max_2hop.csv"

    assert os.path.exists(logs_file), f"Raw data file {logs_file} is missing."
    assert os.path.exists(output_file), f"Output file {output_file} was not created."

    # 1. Compute expected output from the logs file
    edges = []
    with open(logs_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get("status") == "SUCCESS":
                edges.append((record["src"], record["dst"], record["amount"]))

    # Find 1-hop from ROOT
    root_edges = {dst: amount for src, dst, amount in edges if src == "ROOT"}

    # Find 2-hop paths
    max_2hop = defaultdict(int)
    for src, dst, amount in edges:
        if src in root_edges:
            total_amount = root_edges[src] + amount
            if total_amount > max_2hop[dst]:
                max_2hop[dst] = total_amount

    expected_rows = sorted([[dst, str(max_2hop[dst])] for dst in max_2hop.keys()], key=lambda x: x[0])
    expected_header = ["Destination", "MaxTotalAmount"]

    # 2. Read actual output
    actual_data = []
    with open(output_file, "r") as f:
        reader = csv.reader(f)
        try:
            actual_header = next(reader)
        except StopIteration:
            actual_header = []
        for row in reader:
            if row: # ignore empty lines
                actual_data.append(row)

    # 3. Assertions
    assert actual_header == expected_header, f"Header is incorrect. Expected {expected_header}, got {actual_header}"
    assert actual_data == expected_rows, f"Data rows are incorrect. Expected {expected_rows}, got {actual_data}"