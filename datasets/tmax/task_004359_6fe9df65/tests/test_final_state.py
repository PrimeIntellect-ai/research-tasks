# test_final_state.py
import os
import subprocess
import json
import numpy as np
import pandas as pd
import pytest

def test_cron_job():
    try:
        cron_out = subprocess.check_output(["crontab", "-l", "-u", "user"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab for user 'user'.")

    assert "*/5 * * * *" in cron_out, "Crontab does not contain the expected '*/5 * * * *' schedule."
    assert "process_logs.sh" in cron_out, "Crontab does not contain 'process_logs.sh'."

def test_cjson_built():
    assert os.path.exists("/app/cJSON-1.7.15/libcjson.so"), "libcjson.so was not built in /app/cJSON-1.7.15"

def test_config_tracker_executable():
    assert os.path.exists("/home/user/config_tracker"), "/home/user/config_tracker does not exist"
    assert os.access("/home/user/config_tracker", os.X_OK), "/home/user/config_tracker is not executable"

def test_process_logs_script():
    assert os.path.exists("/home/user/process_logs.sh"), "/home/user/process_logs.sh does not exist"
    assert os.access("/home/user/process_logs.sh", os.X_OK), "/home/user/process_logs.sh is not executable"

def test_metric_threshold():
    hidden_test_file = "/tmp/hidden_test.jsonl"
    agent_output_file = "/tmp/agent_output.csv"
    executable = "/home/user/config_tracker"

    # Ensure hidden test data exists
    assert os.path.exists(hidden_test_file), f"Hidden test file {hidden_test_file} missing."

    # Run the agent's executable
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/app/cJSON-1.7.15:" + env.get("LD_LIBRARY_PATH", "")
    try:
        subprocess.run(
            [executable, hidden_test_file, agent_output_file],
            env=env, check=True, timeout=10
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent program crashed or failed to run: {e}")
    except subprocess.TimeoutExpired:
        pytest.fail("Agent program timed out.")

    assert os.path.exists(agent_output_file), f"Agent output file {agent_output_file} was not created."

    # Compute truth
    sizes = []
    truth_records = []
    with open(hidden_test_file) as f:
        for line in f:
            data = json.loads(line)
            size = data['size']
            sizes.append(size)
            window = sizes[-10:]
            mean = np.mean(window)
            std = np.std(window)
            z = 0.0 if std == 0 else (size - mean) / std
            truth_records.append({"timestamp": data['timestamp'], "truth_z": z})

    df_truth = pd.DataFrame(truth_records)

    try:
        df_agent = pd.read_csv(agent_output_file)
    except Exception as e:
        pytest.fail(f"Failed to read agent output CSV: {e}")

    assert 'timestamp' in df_agent.columns, "Agent output missing 'timestamp' column."
    assert 'z_score' in df_agent.columns, "Agent output missing 'z_score' column."

    df_merged = pd.merge(df_truth, df_agent, on='timestamp')
    assert len(df_merged) == len(df_truth), "Agent output does not have the correct number of records or timestamps do not match."

    mse = np.mean((df_merged['truth_z'] - df_merged['z_score']) ** 2)
    threshold = 1e-5

    assert mse < threshold, f"MSE threshold not met. Measured MSE: {mse}, Threshold: < {threshold}"