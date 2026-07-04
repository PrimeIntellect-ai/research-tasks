# test_final_state.py

import os
import pandas as pd
from sklearn.metrics import f1_score

def test_vulnerable_audit_csv_exists():
    """Verify that the agent generated the required output CSV file."""
    output_path = '/home/user/vulnerable_audit.csv'
    assert os.path.exists(output_path), f"The output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"The path {output_path} is not a file."
    assert os.path.getsize(output_path) > 0, f"The output file {output_path} is empty."

def test_vulnerable_audit_f1_score():
    """Verify that the agent's output achieves an F1-score >= 0.95 against the ground truth."""
    ground_truth_path = '/truth/ground_truth.csv'
    agent_output_path = '/home/user/vulnerable_audit.csv'

    assert os.path.exists(ground_truth_path), f"Ground truth file missing: {ground_truth_path}"
    assert os.path.exists(agent_output_path), f"Agent output file missing: {agent_output_path}"

    ground_truth = pd.read_csv(ground_truth_path)
    try:
        agent_output = pd.read_csv(agent_output_path)
    except Exception as e:
        assert False, f"Failed to read agent output CSV: {e}"

    required_cols = ['token_id', 'vulnerability_type', 'associated_ssh_fingerprint']
    for col in required_cols:
        assert col in agent_output.columns, f"Agent output is missing required column: '{col}'"

    # Merge on token_id, filling missing with 'none'
    merged = pd.merge(ground_truth, agent_output, on='token_id', how='outer', suffixes=('_true', '_pred'))
    merged['vulnerability_type_true'] = merged['vulnerability_type_true'].fillna('none')
    merged['vulnerability_type_pred'] = merged['vulnerability_type_pred'].fillna('none')

    # Calculate macro-averaged F1-score
    f1 = f1_score(merged['vulnerability_type_true'], merged['vulnerability_type_pred'], average='macro')

    assert f1 >= 0.95, f"F1-score {f1:.4f} is below the 0.95 threshold. The agent did not correctly classify the vulnerabilities."