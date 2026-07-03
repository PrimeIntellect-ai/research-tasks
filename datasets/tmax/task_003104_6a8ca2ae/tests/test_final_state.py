# test_final_state.py

import os
import re
import pytest
from collections import defaultdict

LOG_FILE = "/home/user/data/sensor_raw.log"
AGG_CSV = "/home/user/output/aggregated.csv"
ETL_LOG = "/home/user/output/etl.log"
GATE_PASSED = "/home/user/output/quality_gate_passed"
GATE_FAILED = "/home/user/output/quality_gate_failed"

def get_expected_data():
    total = 0
    valid = 0
    invalid = 0
    agg = defaultdict(lambda: {'temps': [], 'hums': []})

    if not os.path.exists(LOG_FILE):
        return 0, 0, 0, []

    with open(LOG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            m = re.match(r'\[(.*?)\] SENSOR_LOG device=(\S+) temp=([0-9.-]+) hum=([0-9.-]+)', line)
            if not m:
                invalid += 1
                continue

            ts, device, temp_str, hum_str = m.groups()
            try:
                temp = float(temp_str)
                hum = float(hum_str)
            except ValueError:
                invalid += 1
                continue

            if -50.0 <= temp <= 150.0 and 0.0 <= hum <= 100.0:
                valid += 1
                # Truncate to hour: e.g., 2023-10-12T10:15:30Z -> 2023-10-12T10:00:00Z
                # ts format: YYYY-MM-DDThh:mm:ssZ
                bucket = ts[:14] + "00:00Z"
                agg[(bucket, device)]['temps'].append(temp)
                agg[(bucket, device)]['hums'].append(hum)
            else:
                invalid += 1

    csv_lines = []
    for (bucket, device) in sorted(agg.keys()):
        temps = agg[(bucket, device)]['temps']
        hums = agg[(bucket, device)]['hums']
        avg_temp = sum(temps) / len(temps)
        avg_hum = sum(hums) / len(hums)
        csv_lines.append(f"{bucket},{device},{avg_temp:.2f},{avg_hum:.2f}")

    return total, valid, invalid, csv_lines

def test_aggregated_csv():
    """Test that the aggregated CSV matches the expected output exactly."""
    assert os.path.exists(AGG_CSV), f"Output file {AGG_CSV} does not exist."

    _, _, _, expected_csv_lines = get_expected_data()

    with open(AGG_CSV, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_csv_lines, (
        f"Contents of {AGG_CSV} do not match expected.\n"
        f"Expected:\n{chr(10).join(expected_csv_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )

def test_etl_log():
    """Test that the ETL log contains the correct summary counts."""
    assert os.path.exists(ETL_LOG), f"Log file {ETL_LOG} does not exist."

    total, valid, invalid, _ = get_expected_data()
    expected_log_line = f"TOTAL:{total} VALID:{valid} INVALID:{invalid}"

    with open(ETL_LOG, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == 1, f"{ETL_LOG} should contain exactly one line, found {len(actual_lines)}."
    assert actual_lines[0] == expected_log_line, (
        f"ETL log line mismatch.\nExpected: {expected_log_line}\nActual: {actual_lines[0]}"
    )

def test_quality_gate():
    """Test that the correct quality gate file is created based on the invalid ratio."""
    total, _, invalid, _ = get_expected_data()

    if total == 0:
        pytest.skip("No data to test quality gate.")

    ratio = invalid / total

    if ratio > 0.10:
        assert os.path.exists(GATE_FAILED), f"Expected {GATE_FAILED} to exist because invalid ratio is {ratio:.2f} (> 0.10)."
        assert not os.path.exists(GATE_PASSED), f"Expected {GATE_PASSED} to NOT exist because invalid ratio is {ratio:.2f} (> 0.10)."
    else:
        assert os.path.exists(GATE_PASSED), f"Expected {GATE_PASSED} to exist because invalid ratio is {ratio:.2f} (<= 0.10)."
        assert not os.path.exists(GATE_FAILED), f"Expected {GATE_FAILED} to NOT exist because invalid ratio is {ratio:.2f} (<= 0.10)."