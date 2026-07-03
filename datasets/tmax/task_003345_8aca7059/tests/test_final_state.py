# test_final_state.py
import os
import csv
from collections import defaultdict

def test_cpp_source_exists():
    source_path = "/home/user/etl_processor.cpp"
    assert os.path.isfile(source_path), f"C++ source file missing: {source_path}"

def test_summary_stats_correctness():
    raw_path = "/home/user/raw_telemetry.csv"
    out_path = "/home/user/summary_stats.csv"

    assert os.path.isfile(raw_path), f"Raw telemetry missing: {raw_path}"
    assert os.path.isfile(out_path), f"Output file missing: {out_path}"

    # Compute expected results from the input data
    stats = defaultdict(list)
    with open(raw_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 3:
                continue
            sensor_id, ts_str, temp_str = row

            # Validation Constraints
            if not sensor_id.startswith("SN-"):
                continue
            if int(ts_str) <= 0:
                continue
            temp = float(temp_str)
            if not (-50.0 <= temp <= 150.0):
                continue

            stats[sensor_id].append(temp)

    expected_rows = [["sensor_id", "count", "min_temp", "max_temp", "avg_temp"]]
    for sensor_id in sorted(stats.keys()):
        temps = stats[sensor_id]
        count = len(temps)
        min_temp = min(temps)
        max_temp = max(temps)
        avg_temp = sum(temps) / count
        expected_rows.append([
            sensor_id,
            str(count),
            f"{min_temp:.2f}",
            f"{max_temp:.2f}",
            f"{avg_temp:.2f}"
        ])

    expected_content = [",".join(row) for row in expected_rows]

    # Read actual results
    with open(out_path, "r") as f:
        actual_content = f.read().strip().splitlines()

    assert len(actual_content) == len(expected_content), (
        f"Row count mismatch. Expected {len(expected_content)} rows (including header), "
        f"but got {len(actual_content)}."
    )

    for i, (actual_row, expected_row) in enumerate(zip(actual_content, expected_content)):
        assert actual_row.strip() == expected_row, (
            f"Mismatch at row {i+1}.\n"
            f"Expected: {expected_row}\n"
            f"Actual:   {actual_row.strip()}"
        )