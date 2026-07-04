# test_final_state.py

import os
import json
import subprocess
import pandas as pd
import pytest

def test_graph_builder_accuracy():
    events_path = '/home/user/events.csv'
    agent_commands_path = '/home/user/commands.txt'
    binary_path = '/app/graph_builder'

    assert os.path.isfile(events_path), f"Missing {events_path}"
    assert os.path.isfile(agent_commands_path), f"Missing {agent_commands_path}. The pipeline script must generate this file."
    assert os.path.isfile(binary_path), f"Missing {binary_path}"

    # Generate golden expected commands
    df = pd.read_csv(events_path)
    df = df.sort_values(by=['src_node', 'timestamp'])
    df['rolling_avg'] = df.groupby('src_node')['amount'].transform(lambda x: x.rolling(3, min_periods=1).mean())
    filtered = df[df['amount'] > df['rolling_avg']]
    filtered = filtered.sort_values(by=['src_node', 'timestamp'])

    expected_commands_path = '/tmp/expected_commands.txt'
    with open(expected_commands_path, 'w') as f:
        for _, row in filtered.iterrows():
            f.write(f"ADD EDGE {row['src_node']} {row['dst_node']} {row['amount']}\n")

    # Helper to run binary and get committed edges
    def get_committed_edges(commands_file):
        with open(commands_file, 'r') as f:
            result = subprocess.run([binary_path], stdin=f, capture_output=True, text=True, check=True)

        try:
            output = json.loads(result.stdout)
            return output.get("committed_edges", 0)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON output from {binary_path}. Output was: {result.stdout}")

    golden_edges = get_committed_edges(expected_commands_path)
    agent_edges = get_committed_edges(agent_commands_path)

    assert golden_edges > 0, "Golden expected edges should be greater than 0."

    accuracy = agent_edges / golden_edges

    assert accuracy >= 0.99, (
        f"Accuracy metric failed. "
        f"Agent committed edges: {agent_edges}, Golden committed edges: {golden_edges}. "
        f"Accuracy: {accuracy:.4f} (Threshold: >= 0.99)"
    )