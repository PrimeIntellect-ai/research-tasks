# test_final_state.py

import os
import subprocess
import pytest

def test_telemetry_parser_accuracy():
    project_dir = "/home/user/telemetry_parser"
    test_data = "/home/user/hidden_test_packets.bin"
    oracle_bin = "/app/telemetry_oracle"
    agent_bin = os.path.join(project_dir, "target/release/telemetry_parser")

    # Step 1: Compile the agent's code
    build_proc = subprocess.run(
        ["cargo", "build", "--release"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert build_proc.returncode == 0, f"Cargo build failed:\n{build_proc.stderr}"
    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin} after build."

    # Step 2: Run the agent's binary on the hidden test data
    try:
        agent_proc = subprocess.run(
            [agent_bin, test_data],
            capture_output=True,
            text=True,
            timeout=5
        )
        agent_success = (agent_proc.returncode == 0)
        agent_out = agent_proc.stdout.strip().split('\n')
    except subprocess.TimeoutExpired:
        pytest.fail("Agent binary timed out (likely infinite loop). Accuracy metric: 0.0 < 0.99")
    except Exception as e:
        pytest.fail(f"Agent binary crashed: {e}. Accuracy metric: 0.0 < 0.99")

    # Step 3: Run the oracle binary
    oracle_proc = subprocess.run(
        [oracle_bin, test_data],
        capture_output=True,
        text=True
    )
    oracle_out = oracle_proc.stdout.strip().split('\n')

    # Handle empty outputs
    if not oracle_out or oracle_out == ['']:
        oracle_out = []
    if not agent_out or agent_out == ['']:
        agent_out = []

    # Step 4: Calculate accuracy
    matches = sum(1 for a, o in zip(agent_out, oracle_out) if a == o)
    expected_len = len(oracle_out)

    if expected_len == 0:
        accuracy = 1.0 if len(agent_out) == 0 else 0.0
    else:
        accuracy = matches / expected_len

    # Step 5: Assert threshold
    assert accuracy >= 0.99, f"Accuracy metric is {accuracy:.4f}, which is below the threshold of 0.99. Agent output matched {matches} out of {expected_len} lines."