# test_final_state.py

import os
import json
import pytest

def test_deadlock_report_exists_and_correct():
    input_file = "/home/user/transactions.json"
    output_file = "/home/user/deadlock_report.json"

    assert os.path.exists(output_file), f"Output file {output_file} is missing. Did you run your Go program?"
    assert os.path.isfile(output_file), f"{output_file} should be a file."

    assert os.path.exists(input_file), f"Input file {input_file} is missing."
    with open(input_file, "r") as f:
        transactions = json.load(f)

    # Build graph and transaction map
    tx_map = {t["tx_id"]: t for t in transactions}
    graph = {t["tx_id"]: t["waiting_for_tx"] for t in transactions if t["waiting_for_tx"] is not None}

    # Find the cycle using DFS
    visited = set()
    cycle_nodes = set()

    for node in graph:
        if node in visited:
            continue
        curr = node
        curr_path = []
        while curr is not None and curr not in visited:
            visited.add(curr)
            curr_path.append(curr)
            curr = graph.get(curr)

        if curr is not None and curr in curr_path:
            # Cycle detected
            idx = curr_path.index(curr)
            cycle_nodes.update(curr_path[idx:])
            break  # The instructions specify exactly one cycle

    assert cycle_nodes, "No cycle found in the input data, but one was expected."

    # Filter cycle nodes by duration >= 60
    filtered_txs = [tx_map[node] for node in cycle_nodes if tx_map[node]["duration"] >= 60]

    # Sort primarily by duration DESC, then by tx_id ASC
    filtered_txs.sort(key=lambda x: (-x["duration"], x["tx_id"]))

    # Paginate (top 2)
    expected_output = filtered_txs[:2]

    with open(output_file, "r") as f:
        try:
            actual_output = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_file} does not contain valid JSON.")

    assert isinstance(actual_output, list), f"Expected the output to be a JSON array, got {type(actual_output).__name__}."
    assert actual_output == expected_output, (
        f"The contents of {output_file} do not match the expected deadlock report.\n"
        f"Expected: {json.dumps(expected_output, indent=2)}\n"
        f"Actual: {json.dumps(actual_output, indent=2)}"
    )