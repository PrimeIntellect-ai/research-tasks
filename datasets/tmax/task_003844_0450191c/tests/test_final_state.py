# test_final_state.py

import os
import sys
import subprocess
import random
import csv
import json

def test_video_signal_csv():
    # Check if the extracted video signal CSV exists and is formatted properly
    csv_path = "/home/user/video_signal.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, f"File {csv_path} is empty."

        assert header == ["time", "video_val"], f"Invalid header in {csv_path}: {header}"

        rows = list(reader)
        assert len(rows) == 150, f"Expected exactly 150 rows in {csv_path}, found {len(rows)}"

        for idx, row in enumerate(rows):
            assert len(row) == 2, f"Invalid row format at index {idx}: {row}"
            try:
                float(row[0])
                float(row[1])
            except ValueError:
                assert False, f"Non-float values found at index {idx}: {row}"

def test_fuzz_equivalence():
    agent_script = "/home/user/fusion_pipeline.py"
    oracle_bin = "/app/oracle_fusion_pipeline"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} does not exist."

    random.seed(42)

    for i in range(100):
        # Generate data
        times = [round(x * 0.1, 1) for x in range(501)]

        video_times = times.copy()
        # Drop 10% from video_times (50 elements), but keep first and last to avoid NaN at bounds
        drop_video = random.sample(range(1, 500), 50)
        video_data = []
        for j, t in enumerate(video_times):
            if j not in drop_video:
                val = random.uniform(0, 255)
                video_data.append((t, val))

        # Spike 5-15 video_val rows
        num_spikes = random.randint(5, 15)
        spike_indices = random.sample(range(len(video_data)), num_spikes)
        for idx in spike_indices:
            video_data[idx] = (video_data[idx][0], random.uniform(1000, 2000))

        telemetry_times = times.copy()
        drop_telemetry = random.sample(range(501), 50)
        telemetry_data = []
        for j, t in enumerate(telemetry_times):
            if j not in drop_telemetry:
                val = random.uniform(0, 255)
                telemetry_data.append((t, val))

        video_csv = f"/tmp/fuzz_video_{i}.csv"
        telemetry_csv = f"/tmp/fuzz_telemetry_{i}.csv"

        with open(video_csv, "w") as f:
            f.write("time,video_val\n")
            for t, v in video_data:
                f.write(f"{t},{v}\n")

        with open(telemetry_csv, "w") as f:
            f.write("time,telemetry_val\n")
            for t, v in telemetry_data:
                f.write(f"{t},{v}\n")

        window = random.choice([3, 5, 7, 9])
        threshold = random.uniform(10.0, 50.0)

        agent_out_csv = f"/tmp/agent_out_{i}.csv"
        agent_out_log = f"/tmp/agent_log_{i}.json"

        oracle_out_csv = f"/tmp/oracle_out_{i}.csv"
        oracle_out_log = f"/tmp/oracle_log_{i}.json"

        # Run agent
        agent_cmd = [
            sys.executable, agent_script,
            "--video_in", video_csv,
            "--telemetry_in", telemetry_csv,
            "--out_csv", agent_out_csv,
            "--out_log", agent_out_log,
            "--window", str(window),
            "--threshold", str(threshold)
        ]

        # Run oracle
        oracle_cmd = [
            oracle_bin,
            "--video_in", video_csv,
            "--telemetry_in", telemetry_csv,
            "--out_csv", oracle_out_csv,
            "--out_log", oracle_out_log,
            "--window", str(window),
            "--threshold", str(threshold)
        ]

        res_agent = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert res_agent.returncode == 0, f"Agent script failed on run {i}:\n{res_agent.stderr}"

        res_oracle = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert res_oracle.returncode == 0, f"Oracle failed on run {i}:\n{res_oracle.stderr}"

        # Compare CSV
        with open(agent_out_csv) as f: agent_csv_content = f.read()
        with open(oracle_out_csv) as f: oracle_csv_content = f.read()
        assert agent_csv_content == oracle_csv_content, f"CSV output mismatch on run {i}.\nAgent:\n{agent_csv_content[:500]}...\nOracle:\n{oracle_csv_content[:500]}..."

        # Compare JSON
        with open(agent_out_log) as f: agent_json_content = json.load(f)
        with open(oracle_out_log) as f: oracle_json_content = json.load(f)
        assert agent_json_content == oracle_json_content, f"JSON output mismatch on run {i}.\nAgent: {agent_json_content}\nOracle: {oracle_json_content}"