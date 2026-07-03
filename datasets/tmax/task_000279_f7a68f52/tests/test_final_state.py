# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def generate_random_csv(num_rows):
    lines = ["timestamp,video_pkt_size,audio_pkt_size,subtitle_pkt_size,data_pkt_size"]
    for i in range(num_rows):
        timestamp = round(random.uniform(0.0, 100.0), 6)
        row = [f"{timestamp:.6f}"]
        for _ in range(4):
            if random.random() < 0.3:
                row.append("")
            else:
                row.append(str(random.randint(1, 100000)))
        lines.append(",".join(row))
    return "\n".join(lines)

def test_fuzz_equivalence():
    agent_script = "/home/user/reshape_stats.py"
    oracle_script = "/app/oracle_reshape.py"

    assert os.path.exists(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.exists(oracle_script), f"Oracle script missing: {oracle_script}"

    random.seed(42)

    for i in range(200):
        num_rows = random.randint(0, 1000)
        csv_data = generate_random_csv(num_rows)

        # Run oracle
        oracle_proc = subprocess.run(
            ["python3", oracle_script],
            input=csv_data,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}. Stderr: {oracle_proc.stderr}"

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=csv_data,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed on iteration {i}. Stderr: {agent_proc.stderr}"

        # Parse both JSON outputs
        try:
            oracle_json = json.loads(oracle_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle output invalid JSON on iteration {i}")

        try:
            agent_json = json.loads(agent_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Agent output invalid JSON on iteration {i}. Output: {agent_proc.stdout}")

        assert agent_json == oracle_json, (
            f"Mismatch on iteration {i}.\n"
            f"Input CSV rows: {num_rows}\n"
            f"Oracle output: {oracle_json}\n"
            f"Agent output: {agent_json}"
        )

def test_stream_summary_exists_and_valid():
    summary_path = "/home/user/stream_summary.json"
    assert os.path.exists(summary_path), f"Missing final output file: {summary_path}"

    with open(summary_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{summary_path} does not contain valid JSON")

    assert isinstance(data, list), f"{summary_path} should contain a JSON array"