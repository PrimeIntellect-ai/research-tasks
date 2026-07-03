# test_final_state.py

import os
import glob
import pytest

def test_posterior_mean_accuracy():
    """
    Calculates the true posterior mean from the raw logs and compares it 
    to the agent's output in /home/user/posterior_mean.txt.
    """
    # 1. Calculate true sum and N from raw logs
    n = 0
    sum_x = 0.0
    log_files = glob.glob('/home/user/data/raw_logs/*.csv')
    assert len(log_files) > 0, "No raw log files found in /home/user/data/raw_logs/"

    for file in log_files:
        with open(file, 'r') as f:
            lines = f.readlines()[1:]  # Skip header
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) >= 3 and parts[1] == 'SUCCESS' and parts[2] != '':
                    n += 1
                    sum_x += float(parts[2])

    # 2. Perform Bayesian update
    prior_var = 0.1
    prior_mean = 0.5
    lik_var = 0.05

    post_var = 1.0 / ((1.0 / prior_var) + (n / lik_var))
    post_mean = post_var * ((prior_mean / prior_var) + (sum_x / lik_var))

    # 3. Read agent's output
    output_file = '/home/user/posterior_mean.txt'
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    try:
        with open(output_file, 'r') as f:
            agent_val_str = f.read().strip()
            agent_val = float(agent_val_str)
    except ValueError:
        pytest.fail(f"Failed to parse the contents of {output_file} as a float. Found: '{agent_val_str}'")
    except Exception as e:
        pytest.fail(f"Failed to read {output_file}: {e}")

    # 4. Assert metric threshold
    err = abs(agent_val - post_mean)
    threshold = 0.001
    assert err <= threshold, (
        f"Posterior mean absolute error {err:.6f} exceeds threshold {threshold}. "
        f"Agent value: {agent_val}, True value: {post_mean}"
    )

def test_extract_script_fixed():
    """
    Verifies that the vendored extract_valid_metrics.sh script was fixed to properly
    handle values of 0.0 instead of treating them as falsy.
    """
    script_path = '/app/bash-ops-etl-0.1.0/bin/extract_valid_metrics.sh'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    # The original buggy line was: awk -F, 'NR>1 && $2=="SUCCESS" && $3 {print $3}' "$1"
    # It should be changed so that it doesn't drop 0.0 (e.g. $3!="")
    # We check that the buggy condition is no longer present exactly as it was.
    buggy_condition = '&& $3 {'
    assert buggy_condition not in content, (
        f"The script {script_path} still contains the buggy awk condition "
        "that drops valid '0.0' values."
    )