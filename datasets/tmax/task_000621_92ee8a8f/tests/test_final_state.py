# test_final_state.py

import os
import ast
import pytest

def extract_events_from_mock_server():
    """Extracts the events list from the mock server script."""
    server_path = '/home/user/mock_ci_server.py'
    assert os.path.isfile(server_path), f"{server_path} is missing."

    with open(server_path, 'r') as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'events':
                    return ast.literal_eval(node.value)

    pytest.fail("Could not find 'events' list in mock_ci_server.py")

def calculate_expected_cost(events):
    """Calculates the expected cost according to the state machine and rate limit rules."""
    states = ['START', 'BUILD', 'TEST', 'DEPLOY', 'END']
    expected_state_idx = 0
    last_accepted_time = -1
    total_cost = 0.0

    for ev in events:
        event_name = ev['event']
        cost = ev['compute_cost']
        ts = ev['timestamp_ms']

        # Rate limit check: ignore if within 50ms of previously accepted message
        if last_accepted_time != -1 and (ts - last_accepted_time) <= 50:
            continue

        # State machine check: must match expected state
        if event_name == states[expected_state_idx]:
            total_cost += cost
            last_accepted_time = ts
            expected_state_idx = (expected_state_idx + 1) % len(states)

    return total_cost

def test_final_cost_file_exists():
    """Ensure the final output file exists."""
    assert os.path.isfile('/home/user/final_cost.txt'), "The /home/user/final_cost.txt file was not created."

def test_final_cost_value():
    """Verify the calculated cost matches the derived expected cost."""
    events = extract_events_from_mock_server()
    expected_cost = calculate_expected_cost(events)
    expected_cost_str = f"{expected_cost:.2f}"

    with open('/home/user/final_cost.txt', 'r') as f:
        actual_cost_str = f.read().strip()

    assert actual_cost_str == expected_cost_str, (
        f"The calculated cost is incorrect. Expected '{expected_cost_str}', "
        f"but found '{actual_cost_str}' in /home/user/final_cost.txt."
    )