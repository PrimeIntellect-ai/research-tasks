# test_final_state.py

import os
import json
import pytest

def test_output_jsonl_exists_and_correct():
    output_path = "/home/user/output.jsonl"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    records = []
    with open(output_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON line in {output_path}: {line}")

    # Group by sensor_id
    sensors = {}
    for r in records:
        sid = r.get("sensor_id")
        if sid not in sensors:
            sensors[sid] = []
        sensors[sid].append(r)

    assert "S1" in sensors, "Missing sensor S1 data in output."
    assert "S2" in sensors, "Missing sensor S2 data in output."

    s1_data = sensors["S1"]
    s2_data = sensors["S2"]

    # Verify S1
    assert len(s1_data) == 4, "Expected 4 records for S1."
    assert s1_data[0]["timestamp"] == 100
    assert float(s1_data[0]["temperature"]) == 20.0
    assert float(s1_data[0]["moving_avg"]) == 20.0

    assert s1_data[1]["timestamp"] == 110
    assert float(s1_data[1]["temperature"]) == 22.0
    assert float(s1_data[1]["moving_avg"]) == 21.0

    assert s1_data[2]["timestamp"] == 120
    assert float(s1_data[2]["temperature"]) == 24.0
    assert float(s1_data[2]["moving_avg"]) == 22.0

    assert s1_data[3]["timestamp"] == 130
    assert float(s1_data[3]["temperature"]) == 22.0
    assert round(float(s1_data[3]["moving_avg"]), 2) in (22.66, 22.67)

    # Verify S2
    assert len(s2_data) == 2, "Expected 2 records for S2."
    assert s2_data[0]["timestamp"] == 105
    assert float(s2_data[0]["temperature"]) == 15.0
    assert float(s2_data[0]["moving_avg"]) == 15.0

    assert s2_data[1]["timestamp"] == 115
    assert float(s2_data[1]["temperature"]) == 15.5
    assert float(s2_data[1]["moving_avg"]) == 15.25

def test_crontab_exists_and_correct():
    crontab_path = "/home/user/crontab.txt"
    assert os.path.isfile(crontab_path), f"Crontab file {crontab_path} is missing."

    with open(crontab_path, "r") as f:
        content = f.read().strip()

    assert "*/15 * * * *" in content or "0,15,30,45 * * * *" in content, "Crontab does not have the correct schedule (every 15 minutes)."
    assert "go run /home/user/process.go" in content, "Crontab does not execute the correct command."