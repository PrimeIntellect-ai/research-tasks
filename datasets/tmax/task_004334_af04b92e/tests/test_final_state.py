# test_final_state.py

import os
import json

def test_deadlocks_json_exists_and_correct():
    """Test that the deadlocks.json file exists and contains the correct deadlocked transactions."""
    output_file = "/home/user/deadlocks.json"
    input_file = "/home/user/transactions.jsonl"

    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Did you run your Go program?"

    # Recompute the expected deadlocks based on the input file
    assert os.path.isfile(input_file), f"Input file {input_file} is missing."

    acquired = {}
    waiting = {}

    with open(input_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            tx = event["tx_id"]
            action = event["action"]
            res = event["resource"]

            if action == "ACQUIRED":
                acquired[res] = tx
            elif action == "WAITING":
                if tx not in waiting:
                    waiting[tx] = []
                waiting[tx].append(res)

    # Build wait-for graph
    graph = {}
    for tx, res_list in waiting.items():
        for res in res_list:
            if res in acquired:
                target_tx = acquired[res]
                if tx not in graph:
                    graph[tx] = []
                graph[tx].append(target_tx)

    # Detect cycles
    def find_cycles(graph):
        visited = set()
        rec_stack = set()
        deadlocked = set()

        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path)
                elif neighbor in rec_stack:
                    # Cycle detected
                    cycle_start_idx = path.index(neighbor)
                    for n in path[cycle_start_idx:]:
                        deadlocked.add(n)

            rec_stack.remove(node)
            path.pop()

        for node in list(graph.keys()) + list(acquired.values()):
            if node not in visited:
                dfs(node, [])

        return sorted(list(deadlocked))

    expected_deadlocks = find_cycles(graph)

    # Validate the output JSON
    with open(output_file, "r") as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {output_file} does not contain valid JSON."

    assert isinstance(output_data, dict), f"Expected JSON object, got {type(output_data).__name__}"
    assert "deadlocked_transactions" in output_data, "Key 'deadlocked_transactions' is missing from the output JSON."

    actual_deadlocks = output_data["deadlocked_transactions"]
    assert isinstance(actual_deadlocks, list), f"Expected 'deadlocked_transactions' to be a list, got {type(actual_deadlocks).__name__}"

    assert actual_deadlocks == expected_deadlocks, f"Deadlocked transactions mismatch. Expected {expected_deadlocks}, got {actual_deadlocks}"