# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_transcription_file():
    path = "/home/user/transcribed_alert.txt"
    assert os.path.isfile(path), f"Missing transcription file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    expected = "The network connectivity has failed with storage error code ENOSPC"
    assert content == expected, f"Transcription content mismatch. Expected '{expected}', got '{content}'"

def generate_random_logs(num_lines=100):
    lines = []
    for _ in range(num_lines):
        date = f"2023-10-{random.randint(10, 31)}"
        time = f"{random.randint(10, 23)}:{random.randint(10, 59)}:{random.randint(10, 59)}"
        pid = random.randint(1000, 9999)
        level = random.choice(["INFO", "WARN", "CRITICAL"])
        msg = ''.join(random.choices(string.ascii_letters, k=15))
        lines.append(f"{date} {time} {pid} {level} {msg}")
    return "\n".join(lines) + "\n"

def test_parse_metrics_fuzz_equivalence():
    agent_script = "/home/user/parse_metrics.sh"
    oracle_script = "/app/bin/oracle_parse_metrics"

    assert os.path.isfile(agent_script), f"Missing agent script: {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script is not executable: {agent_script}"

    random.seed(42)

    for i in range(500):
        input_data = generate_random_logs(100)

        oracle_proc = subprocess.run(
            [oracle_script],
            input=input_data,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run(
            [agent_script],
            input=input_data,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed with return code {agent_proc.returncode}\nStderr: {agent_proc.stderr}"
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on iteration {i}.\n"
                f"Input:\n{input_data}\n"
                f"Oracle Output:\n{oracle_out}\n"
                f"Agent Output:\n{agent_out}"
            )

def test_run_alerts_execution():
    wrapper_script = "/home/user/run_alerts.sh"
    output_log = "/home/user/alert_output.log"

    assert os.path.isfile(wrapper_script), f"Missing wrapper script: {wrapper_script}"
    assert os.access(wrapper_script, os.X_OK), f"Wrapper script is not executable: {wrapper_script}"

    # Remove output log if it exists to ensure we test the script's creation of it
    if os.path.exists(output_log):
        os.remove(output_log)

    proc = subprocess.run(
        [wrapper_script],
        capture_output=True,
        text=True
    )
    assert proc.returncode == 0, f"Wrapper script failed. Stderr: {proc.stderr}"

    assert os.path.isfile(output_log), f"Output log was not created at {output_log}"

    with open(output_log, "r") as f:
        content = f.read()

    assert "mnt/data" in content or "0" in content, "Output log does not seem to contain `du` output."
    assert "ENOSPC" in content, "Output log does not seem to contain parsed metrics."