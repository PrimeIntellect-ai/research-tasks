# test_final_state.py

import os
import csv
import random
from collections import defaultdict

def compute_expected_results():
    random.seed(42)
    servers = [f"server_{i:03d}" for i in range(10)]
    base_config = {f"key{i}": "val0" for i in range(10)}

    records = []
    for file_idx in range(3):
        for t in range(20):
            for s in servers:
                ts = 1600000000 + t * 3600 + file_idx * 86400 + random.randint(0, 60)
                cfg = base_config.copy()

                # Replicate the exact random sequence from setup
                r1 = random.random()
                if r1 < 0.2:
                    cfg[f"key{random.randint(0, 9)}"] = f"val{random.randint(1, 5)}"
                else:
                    r2 = random.random()
                    if r2 < 0.05:
                        for k in range(5):
                            cfg[f"key{random.randint(0, 9)}"] = f"val{random.randint(10, 20)}"

                records.append({"server_id": s, "timestamp": ts, "config": cfg})

    grouped = defaultdict(list)
    for r in records:
        grouped[r["server_id"]].append(r)

    results = []
    for s in sorted(grouped.keys()):
        server_records = sorted(grouped[s], key=lambda x: x["timestamp"])
        sims = []
        for i in range(len(server_records) - 1):
            cfg1 = set(f"{k}={v}" for k, v in server_records[i]["config"].items())
            cfg2 = set(f"{k}={v}" for k, v in server_records[i+1]["config"].items())
            sim = len(cfg1 & cfg2) / len(cfg1 | cfg2)
            sims.append(sim)
            window = sims[-3:]
            rolling_avg = sum(window) / len(window)
            results.append((s, server_records[i+1]["timestamp"], sim, rolling_avg))

    results.sort(key=lambda x: (x[0], x[1]))
    return results

def test_config_analyzer_script_exists():
    assert os.path.isfile("/home/user/config_analyzer.py"), "The script /home/user/config_analyzer.py does not exist."

def test_results_csv_contents():
    results_path = "/home/user/results.csv"
    assert os.path.isfile(results_path), f"The file {results_path} does not exist."

    expected_results = compute_expected_results()

    with open(results_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["server_id", "timestamp", "similarity", "rolling_avg"], "Incorrect header in results.csv."

        rows = list(reader)
        assert len(rows) == len(expected_results), f"Expected {len(expected_results)} rows in results.csv, but got {len(rows)}."

        for i, (row, exp) in enumerate(zip(rows, expected_results)):
            assert row[0] == exp[0], f"Row {i+1}: expected server_id {exp[0]}, got {row[0]}"
            assert int(row[1]) == exp[1], f"Row {i+1}: expected timestamp {exp[1]}, got {row[1]}"
            assert f"{float(row[2]):.4f}" == f"{exp[2]:.4f}", f"Row {i+1}: expected similarity {exp[2]:.4f}, got {row[2]}"
            assert f"{float(row[3]):.4f}" == f"{exp[3]:.4f}", f"Row {i+1}: expected rolling_avg {exp[3]:.4f}, got {row[3]}"

def test_alerts_csv_contents():
    alerts_path = "/home/user/alerts.csv"
    assert os.path.isfile(alerts_path), f"The file {alerts_path} does not exist."

    expected_results = compute_expected_results()
    expected_alerts = [exp for exp in expected_results if exp[3] < 0.5000]

    with open(alerts_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["server_id", "timestamp", "similarity", "rolling_avg"], "Incorrect header in alerts.csv."

        rows = list(reader)
        assert len(rows) == len(expected_alerts), f"Expected {len(expected_alerts)} rows in alerts.csv, but got {len(rows)}."

        for i, (row, exp) in enumerate(zip(rows, expected_alerts)):
            assert row[0] == exp[0], f"Row {i+1}: expected server_id {exp[0]}, got {row[0]}"
            assert int(row[1]) == exp[1], f"Row {i+1}: expected timestamp {exp[1]}, got {row[1]}"
            assert f"{float(row[2]):.4f}" == f"{exp[2]:.4f}", f"Row {i+1}: expected similarity {exp[2]:.4f}, got {row[2]}"
            assert f"{float(row[3]):.4f}" == f"{exp[3]:.4f}", f"Row {i+1}: expected rolling_avg {exp[3]:.4f}, got {row[3]}"