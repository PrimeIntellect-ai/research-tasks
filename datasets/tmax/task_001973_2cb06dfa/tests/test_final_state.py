# test_final_state.py
import os
import csv
import math
import stat
import pytest

def get_expected_data():
    weights_path = "/home/user/weights.txt"
    data_path = "/home/user/sensor_data.csv"

    w_temp, w_press, bias = 0.0, 0.0, 0.0
    with open(weights_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("w_temp="):
                w_temp = float(line.split("=")[1])
            elif line.startswith("w_press="):
                w_press = float(line.split("=")[1])
            elif line.startswith("bias="):
                bias = float(line.split("=")[1])

    expected_scored = []
    sensor_scores = {1: [], 2: [], 3: []}

    with open(data_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensor_id_str = row["sensor_id"].strip()
            if sensor_id_str not in ["1", "2", "3"]:
                continue
            sensor_id = int(sensor_id_str)

            pressure_str = row["pressure"].strip()
            if not pressure_str:
                continue
            try:
                pressure = float(pressure_str)
            except ValueError:
                continue

            temp_str = row["temperature"].strip()
            temp = 20.0
            if temp_str and temp_str.lower() != "nan":
                try:
                    parsed_temp = float(temp_str)
                    if -50.0 <= parsed_temp <= 150.0:
                        temp = parsed_temp
                except ValueError:
                    pass

            risk_score = (temp * w_temp) + (pressure * w_press) + bias
            expected_scored.append({
                "timestamp": row["timestamp"],
                "sensor_id": sensor_id_str,
                "risk_score": risk_score
            })
            sensor_scores[sensor_id].append(risk_score)

    expected_summary = {}
    for sid, scores in sensor_scores.items():
        if scores:
            avg = sum(scores) / len(scores)
            expected_summary[sid] = avg

    return expected_scored, expected_summary

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"Pipeline script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Pipeline script {script_path} is not executable."

def test_scorer_c_exists():
    c_path = "/home/user/scorer.c"
    assert os.path.exists(c_path), f"C source file {c_path} does not exist."

def test_scored_data_csv():
    output_path = "/home/user/scored_data.csv"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    expected_scored, _ = get_expected_data()

    with open(output_path, "r") as f:
        reader = csv.DictReader(f)
        actual_rows = list(reader)

    assert "timestamp" in reader.fieldnames and "sensor_id" in reader.fieldnames and "risk_score" in reader.fieldnames, \
        "Header in scored_data.csv is incorrect."

    assert len(actual_rows) == len(expected_scored), f"Expected {len(expected_scored)} rows, got {len(actual_rows)}."

    for actual, expected in zip(actual_rows, expected_scored):
        assert actual["timestamp"] == expected["timestamp"], "Timestamp mismatch."
        assert actual["sensor_id"] == expected["sensor_id"], "Sensor ID mismatch."

        expected_score_str = f"{expected['risk_score']:.2f}"
        actual_score = float(actual["risk_score"])
        expected_score = float(expected_score_str)

        assert math.isclose(actual_score, expected_score, abs_tol=0.015), \
            f"Risk score mismatch for timestamp {actual['timestamp']}: expected {expected_score_str}, got {actual['risk_score']}."

def test_summary_txt():
    summary_path = "/home/user/summary.txt"
    assert os.path.exists(summary_path), f"Summary file {summary_path} does not exist."

    _, expected_summary = get_expected_data()

    actual_summary = {}
    with open(summary_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            if len(parts) == 2:
                sid = int(parts[0].strip())
                val = float(parts[1].strip())
                actual_summary[sid] = val

    for sid in [1, 2, 3]:
        if sid in expected_summary:
            assert sid in actual_summary, f"Sensor ID {sid} missing from summary.txt."
            expected_val_str = f"{expected_summary[sid]:.2f}"
            expected_val = float(expected_val_str)
            assert math.isclose(actual_summary[sid], expected_val, abs_tol=0.015), \
                f"Average score mismatch for sensor {sid}: expected {expected_val_str}, got {actual_summary[sid]}."