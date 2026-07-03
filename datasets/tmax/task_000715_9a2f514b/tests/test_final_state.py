# test_final_state.py
import os
import csv
import random
import subprocess
import tempfile
import pytest

def test_video_stats_csv():
    csv_path = "/home/user/video_stats.csv"
    assert os.path.isfile(csv_path), f"Missing {csv_path}"

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['frame_index', 'timestamp_ms', 'avg_brightness'], "Incorrect headers in video_stats.csv"

        rows = list(reader)
        assert len(rows) == 1500, f"Expected 1500 rows in video_stats.csv, found {len(rows)}"

def test_joined_dataset_csv():
    csv_path = "/home/user/joined_dataset.csv"
    assert os.path.isfile(csv_path), f"Missing {csv_path}"

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['timestamp_ms', 'avg_brightness', 'sensor_value'], "Incorrect headers in joined_dataset.csv"

def test_model_result():
    result_path = "/home/user/model_result.txt"
    assert os.path.isfile(result_path), f"Missing {result_path}"

    with open(result_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        try:
            val = float(content)
        except ValueError:
            pytest.fail(f"Content of {result_path} is not a valid float: {content}")

def test_join_stats_fuzz_equivalence():
    agent_bin = "/home/user/join_stats"
    oracle_bin = "/app/oracle_join_stats"

    assert os.path.isfile(agent_bin), f"Missing agent binary at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"
    assert os.path.isfile(oracle_bin), f"Missing oracle binary at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary at {oracle_bin} is not executable"

    random.seed(42)
    N = 500

    with tempfile.TemporaryDirectory() as tmpdir:
        csv1_path = os.path.join(tmpdir, "csv1.csv")
        csv2_path = os.path.join(tmpdir, "csv2.csv")

        for i in range(N):
            num_rows_1 = random.randint(0, 500)
            num_rows_2 = random.randint(0, 500)

            with open(csv1_path, 'w', encoding='utf-8') as f1:
                f1.write("frame_index,timestamp_ms,avg_brightness\n")
                for r in range(num_rows_1):
                    ts = random.randint(0, 1000) * 40
                    f1.write(f"{r},{ts},{random.uniform(0, 255):.2f}\n")

            with open(csv2_path, 'w', encoding='utf-8') as f2:
                f2.write("timestamp_ms,sensor_value\n")
                for r in range(num_rows_2):
                    ts = random.randint(0, 1000) * 40
                    f2.write(f"{ts},{random.uniform(-10, 10):.4f}\n")

            oracle_proc = subprocess.run(
                [oracle_bin, csv1_path, csv2_path],
                capture_output=True,
                text=True
            )

            agent_proc = subprocess.run(
                [agent_bin, csv1_path, csv2_path],
                capture_output=True,
                text=True
            )

            if oracle_proc.returncode != agent_proc.returncode or oracle_proc.stdout != agent_proc.stdout:
                with open(csv1_path, 'r') as f:
                    csv1_content = f.read()
                with open(csv2_path, 'r') as f:
                    csv2_content = f.read()

                pytest.fail(
                    f"Fuzz equivalence failed on iteration {i}.\n"
                    f"CSV 1:\n{csv1_content[:500]}...\n"
                    f"CSV 2:\n{csv2_content[:500]}...\n"
                    f"Oracle Return Code: {oracle_proc.returncode}\n"
                    f"Agent Return Code: {agent_proc.returncode}\n"
                    f"Oracle Output (first 500 chars):\n{oracle_proc.stdout[:500]}\n"
                    f"Agent Output (first 500 chars):\n{agent_proc.stdout[:500]}\n"
                )