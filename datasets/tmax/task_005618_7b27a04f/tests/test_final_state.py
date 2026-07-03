# test_final_state.py

import os
import csv
import math
from collections import defaultdict

def test_rust_project_exists():
    cargo_toml = "/home/user/etl_pipeline/Cargo.toml"
    assert os.path.exists(cargo_toml), f"Rust project manifest not found at {cargo_toml}. Did you create the project?"

def test_output_file_exists():
    output_csv = "/home/user/data_warehouse/aggregated_stats.csv"
    assert os.path.exists(output_csv), f"Output CSV not found at {output_csv}. Did you create the data_warehouse directory and write the file?"

def test_csv_contents():
    raw_logs = "/home/user/raw_logs.txt"
    output_csv = "/home/user/data_warehouse/aggregated_stats.csv"

    # Parse raw logs to derive the expected ground truth
    data = defaultdict(list)
    with open(raw_logs, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Format: [YYYY-MM-DD HH:MM:SS] <IP_ADDRESS> - <ENDPOINT> - <STATUS_CODE> - <RESPONSE_TIME_MS>ms
            parts = line.split(' - ')
            if len(parts) >= 4:
                endpoint = parts[1]
                status = parts[2]
                if status == '500':
                    continue
                time_ms = float(parts[3].replace('ms', ''))
                data[endpoint].append(time_ms)

    expected_stats = {}
    for endpoint, times in data.items():
        n = len(times)
        mean = sum(times) / n
        if n > 1:
            variance = sum((x - mean) ** 2 for x in times) / (n - 1)
            std_dev = math.sqrt(variance)
            margin = 1.96 * (std_dev / math.sqrt(n))
        else:
            margin = 0.0

        expected_stats[endpoint] = {
            'count': n,
            'mean': round(mean, 2),
            'ci_lower': round(mean - margin, 2),
            'ci_upper': round(mean + margin, 2)
        }

    # Read the generated CSV
    with open(output_csv, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, f"The CSV file {output_csv} is empty."

        expected_header = ['endpoint', 'count', 'mean', 'ci_lower', 'ci_upper']
        assert header == expected_header, f"Incorrect CSV header. Expected {expected_header}, got {header}"

        rows = list(reader)

    # Check sorting
    endpoints_in_csv = [row[0] for row in rows]
    assert endpoints_in_csv == sorted(endpoints_in_csv), "CSV rows are not sorted alphabetically by the 'endpoint' column."

    assert len(rows) == len(expected_stats), f"Expected {len(expected_stats)} rows in the CSV, but found {len(rows)}."

    for row in rows:
        assert len(row) == 5, f"Expected 5 columns in row, got {len(row)}: {row}"
        endpoint = row[0]
        count = int(row[1])
        mean = float(row[2])
        ci_lower = float(row[3])
        ci_upper = float(row[4])

        assert endpoint in expected_stats, f"Unexpected endpoint found in CSV: {endpoint}"
        exp = expected_stats[endpoint]

        assert count == exp['count'], f"For endpoint {endpoint}: expected count {exp['count']}, got {count}"
        assert math.isclose(mean, exp['mean'], abs_tol=0.01), f"For endpoint {endpoint}: expected mean {exp['mean']}, got {mean}"
        assert math.isclose(ci_lower, exp['ci_lower'], abs_tol=0.01), f"For endpoint {endpoint}: expected ci_lower {exp['ci_lower']}, got {ci_lower}"
        assert math.isclose(ci_upper, exp['ci_upper'], abs_tol=0.01), f"For endpoint {endpoint}: expected ci_upper {exp['ci_upper']}, got {ci_upper}"