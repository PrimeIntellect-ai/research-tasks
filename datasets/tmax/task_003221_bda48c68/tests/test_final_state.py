# test_final_state.py

import json
import os
import pytest

def test_settings_fixed():
    """Check if the REDIS_URL was fixed in settings.env."""
    settings_path = '/home/user/services/config_api/settings.env'
    assert os.path.exists(settings_path), f"{settings_path} does not exist"
    with open(settings_path, 'r') as f:
        content = f.read()
    assert 'REDIS_URL=redis://127.0.0.1:6379' in content, "REDIS_URL was not correctly fixed to port 6379 in settings.env"

def test_processed_events_exists():
    """Check if the processed events file was created."""
    assert os.path.exists('/home/user/processed_events.jsonl'), "/home/user/processed_events.jsonl is missing"

def test_imputation_mse():
    """Calculate MSE of imputed cpu_limit and mem_limit against ground truth and assert threshold."""
    ground_truth_path = '/var/opt/ground_truth.jsonl'
    processed_path = '/home/user/processed_events.jsonl'

    assert os.path.exists(ground_truth_path), f"{ground_truth_path} is missing"
    assert os.path.exists(processed_path), f"{processed_path} is missing"

    ground_truth = {}
    with open(ground_truth_path, 'r') as f:
        for line in f:
            if not line.strip(): continue
            ev = json.loads(line)
            ground_truth[ev['event_id']] = ev

    processed = {}
    with open(processed_path, 'r') as f:
        for line in f:
            if not line.strip(): continue
            ev = json.loads(line)
            processed[ev['event_id']] = ev

    assert len(processed) > 0, "No processed events found in output file."

    sq_errors = []
    for eid, p_ev in processed.items():
        if eid in ground_truth:
            gt_ev = ground_truth[eid]

            p_cpu = p_ev.get('cpu_limit')
            gt_cpu = gt_ev.get('cpu_limit')
            if p_cpu is not None and gt_cpu is not None:
                sq_errors.append((float(p_cpu) - float(gt_cpu)) ** 2)

            p_mem = p_ev.get('mem_limit')
            gt_mem = gt_ev.get('mem_limit')
            if p_mem is not None and gt_mem is not None:
                sq_errors.append((float(p_mem) - float(gt_mem)) ** 2)

    assert len(sq_errors) > 0, "No matching events with numeric limits found for MSE calculation."

    mse = sum(sq_errors) / len(sq_errors)
    assert mse <= 0.5, f"Imputation MSE is {mse:.4f}, which is strictly greater than the threshold of 0.5."

def test_reports_sent():
    """Check if reports were successfully posted to the receiver."""
    reports_path = '/tmp/reports.json'
    assert os.path.exists(reports_path), "Reports were not saved to /tmp/reports.json by the receiver app. Did you POST to the correct endpoint?"

    with open(reports_path, 'r') as f:
        content = f.read().strip()

    assert len(content) > 0, "Reports file is empty. No valid payloads were received."