# test_final_state.py
import os
import pytest

def test_f1_score_meets_threshold():
    agent_file = '/home/user/clean_events.txt'
    golden_file = '/tmp/golden_events.txt'

    assert os.path.exists(agent_file), f"Agent output file {agent_file} does not exist. Did you run the ETL script?"
    assert os.path.exists(golden_file), f"Golden reference file {golden_file} does not exist."

    with open(agent_file, 'r') as f:
        agent_data = set(line.strip() for line in f if line.strip())

    with open(golden_file, 'r') as f:
        golden_data = set(line.strip() for line in f if line.strip())

    if not agent_data:
        f1 = 0.0
    else:
        true_positives = len(agent_data.intersection(golden_data))
        false_positives = len(agent_data - golden_data)
        false_negatives = len(golden_data - agent_data)

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

        if precision + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.98, f"F1 score is {f1:.4f}, which is below the required threshold of 0.98. Precision: {precision:.4f}, Recall: {recall:.4f}"

def test_etl_log_exists():
    log_file = '/home/user/etl.log'
    assert os.path.exists(log_file), f"ETL log file {log_file} does not exist. The task requires maintaining a log of the pipeline."
    assert os.path.getsize(log_file) > 0, f"ETL log file {log_file} is empty. It should document lines read, duplicates dropped, and lines written."