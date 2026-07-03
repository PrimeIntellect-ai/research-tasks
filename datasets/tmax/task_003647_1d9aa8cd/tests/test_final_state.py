# test_final_state.py

import os
import subprocess
import time
import pytest

def test_fast_motif_exists():
    agent_script = "/home/user/fast_motif.py"
    assert os.path.exists(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.isfile(agent_script), f"Not a file: {agent_script}"

def test_fast_motif_performance_and_accuracy():
    eval_file = "/home/user/eval_edges.tsv"
    agent_script = "/home/user/fast_motif.py"
    oracle_bin = "/app/motif_oracle"

    assert os.path.exists(eval_file), f"Evaluation dataset missing: {eval_file}"
    assert os.path.exists(oracle_bin), f"Oracle binary missing: {oracle_bin}"

    # Run Oracle
    start_oracle = time.time()
    try:
        oracle_out = subprocess.check_output([oracle_bin, eval_file], text=True).splitlines()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle execution failed: {e}")
    oracle_time = time.time() - start_oracle

    # Run Agent Python Script
    start_agent = time.time()
    try:
        agent_out = subprocess.check_output(['python3', agent_script, eval_file], text=True).splitlines()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent script execution failed: {e}")
    agent_time = time.time() - start_agent

    # Calculate F1
    oracle_set = set(x.strip() for x in oracle_out if x.strip())
    agent_set = set(x.strip() for x in agent_out if x.strip())

    true_positives = len(oracle_set.intersection(agent_set))
    if len(oracle_set) == 0 and len(agent_set) == 0:
        f1 = 1.0
    elif len(oracle_set) == 0 or len(agent_set) == 0:
        f1 = 0.0
    else:
        precision = true_positives / len(agent_set)
        recall = true_positives / len(oracle_set)
        if (precision + recall) > 0:
            f1 = 2 * (precision * recall) / (precision + recall)
        else:
            f1 = 0.0

    speedup = oracle_time / max(agent_time, 0.001)

    assert f1 >= 0.99, f"F1 Score {f1:.4f} failed to meet 0.99 threshold. Oracle found {len(oracle_set)} nodes, agent found {len(agent_set)} nodes."
    assert speedup >= 50.0, f"Speedup {speedup:.2f}x failed to meet 50.0x threshold. Oracle time: {oracle_time:.4f}s, Agent time: {agent_time:.4f}s."