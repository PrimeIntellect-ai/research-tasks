# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_extracted_metrics_mse():
    """Verify that the extracted metrics CSV meets the MSE threshold."""
    agent_csv = '/home/user/extracted_metrics.csv'
    gt_csv = '/app/ground_truth_metrics.csv'

    assert os.path.isfile(agent_csv), f"Agent's output file is missing: {agent_csv}"
    assert os.path.isfile(gt_csv), f"Ground truth metrics file is missing: {gt_csv}"

    df_agent = pd.read_csv(agent_csv)
    df_gt = pd.read_csv(gt_csv)

    assert 'frame' in df_agent.columns, "Agent CSV must have a 'frame' column"
    assert 'red_pct' in df_agent.columns, "Agent CSV must have a 'red_pct' column"

    agent_vals = df_agent['red_pct'].values
    gt_vals = df_gt['red_pct'].values

    expected_min_len = int(len(gt_vals) * 0.9)
    assert len(agent_vals) >= expected_min_len, f"Agent extracted {len(agent_vals)} frames, expected at least {expected_min_len}"

    min_len = min(len(agent_vals), len(gt_vals))
    mse = np.mean((agent_vals[:min_len] - gt_vals[:min_len])**2)

    assert mse <= 1.5, f"MSE {mse:.4f} exceeds threshold 1.5. Extracted metrics are not accurate enough."

def test_monitor_service_exists():
    """Check that the monitor_service.py script exists."""
    script_path = '/home/user/monitor_service.py'
    assert os.path.isfile(script_path), f"Monitor service script is missing: {script_path}"

def test_supervisord_conf():
    """Check that supervisord.conf is properly configured."""
    conf_path = '/home/user/supervisord.conf'
    assert os.path.isfile(conf_path), f"supervisord.conf is missing: {conf_path}"

    with open(conf_path, 'r') as f:
        content = f.read().lower()

    assert 'monitor_service.py' in content, "supervisord.conf does not mention monitor_service.py"

    # Remove all whitespace to check for autorestart setting flexibly
    content_no_spaces = content.replace(' ', '').replace('\t', '')
    assert 'autorestart=true' in content_no_spaces, "supervisord.conf must have autorestart=true configured"

def test_logrotate_conf():
    """Check that logrotate.conf is properly configured."""
    conf_path = '/home/user/logrotate.conf'
    assert os.path.isfile(conf_path), f"logrotate.conf is missing: {conf_path}"

    with open(conf_path, 'r') as f:
        content = f.read().lower()

    assert '/home/user/logs/monitor.log' in content, "logrotate.conf must manage /home/user/logs/monitor.log"

    # Check required directives
    directives = ['daily', 'rotate 3', 'compress', 'missingok']
    for directive in directives:
        # For rotate 3, allow any whitespace between rotate and 3
        if directive == 'rotate 3':
            assert 'rotate' in content and '3' in content, "logrotate.conf must specify 'rotate 3'"
        else:
            assert directive in content, f"logrotate.conf is missing directive: {directive}"