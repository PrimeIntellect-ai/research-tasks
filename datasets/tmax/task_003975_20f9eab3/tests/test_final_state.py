# test_final_state.py

import os
import csv
import math

def test_anomalies_file_exists_and_correct():
    input_file = "/home/user/system_metrics.csv"
    output_file = "/home/user/anomalies.csv"

    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.exists(input_file), f"Input file {input_file} is missing."

    # Recompute expected output
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        metrics = {"cpu": [], "memory": [], "disk": []}
        records = []
        for row in reader:
            ts = int(row["timestamp"])
            for m in ["cpu", "memory", "disk"]:
                val = float(row[m])
                if val >= 0.0:
                    metrics[m].append(val)
                    records.append({"timestamp": ts, "metric": m, "value": val})

    stats = {}
    for m, vals in metrics.items():
        n = len(vals)
        if n == 0:
            continue
        mean = sum(vals) / n
        variance = sum((x - mean) ** 2 for x in vals) / n
        stddev = math.sqrt(variance)
        stats[m] = {"mean": mean, "stddev": stddev}

    anomalies = []
    for r in records:
        m = r["metric"]
        val = r["value"]
        if abs(val - stats[m]["mean"]) > 2 * stats[m]["stddev"]:
            anomalies.append(r)

    anomalies.sort(key=lambda x: (x["timestamp"], x["metric"]))

    expected_rows = [["timestamp", "metric", "value"]]
    for a in anomalies:
        expected_rows.append([str(a["timestamp"]), a["metric"], f"{a['value']:.1f}"])

    with open(output_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) > 0, f"{output_file} is empty."
    assert actual_rows[0] == expected_rows[0], f"Header row in {output_file} is incorrect."
    assert actual_rows == expected_rows, f"Anomalies in {output_file} do not match the expected values."