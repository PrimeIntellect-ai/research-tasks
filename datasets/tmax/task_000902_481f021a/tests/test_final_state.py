# test_final_state.py

import os
import csv
import json
import math
import pytest

def test_processed_data_exists_and_format():
    processed_path = "/home/user/data/processed_data.csv"
    assert os.path.exists(processed_path), "Processed data file is missing."

    with open(processed_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "Processed data is empty."

        expected_cols = ["id", "text", "value_1", "value_2", "target", "seq_length"]
        for col in expected_cols:
            assert col in header, f"Missing column '{col}' in processed_data.csv"

        rows = list(reader)
        assert len(rows) == 1000, f"Expected 1000 rows, found {len(rows)}."

def test_processed_data_values():
    raw_path = "/home/user/data/raw_data.csv"
    processed_path = "/home/user/data/processed_data.csv"

    raw_v1 = []
    raw_v2 = []
    with open(raw_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["value_1"]:
                raw_v1.append(float(row["value_1"]))
            raw_v2.append(float(row["value_2"]))

    raw_v1.sort()
    # Median calculation
    n = len(raw_v1)
    if n % 2 == 0:
        median_v1 = (raw_v1[n//2 - 1] + raw_v1[n//2]) / 2.0
    else:
        median_v1 = raw_v1[n//2]

    raw_v2.sort()
    # Approximate 5th and 95th percentiles (numpy default linear interpolation)
    def get_percentile(data, p):
        k = (len(data) - 1) * (p / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return data[int(k)]
        d0 = data[int(f)] * (c - k)
        d1 = data[int(c)] * (k - f)
        return d0 + d1

    p5 = get_percentile(raw_v2, 5)
    p95 = get_percentile(raw_v2, 95)

    with open(processed_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check value_1 imputation
            v1 = float(row["value_1"])
            assert not math.isnan(v1), "value_1 contains NaN"

            # Check value_2 clipping
            v2 = float(row["value_2"])
            assert v2 >= p5 - 1e-5, f"value_2 not clipped at 5th percentile: {v2} < {p5}"
            assert v2 <= p95 + 1e-5, f"value_2 not clipped at 95th percentile: {v2} > {p95}"

            # Check seq_length
            text = row["text"]
            seq_len = int(row["seq_length"])
            assert seq_len == len(text.split()), f"seq_length incorrect for text: '{text}'"

def test_metrics_json():
    metrics_path = "/home/user/metrics.json"
    assert os.path.exists(metrics_path), "metrics.json is missing."

    with open(metrics_path, "r", encoding="utf-8") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("metrics.json is not valid JSON.")

    assert "mse" in metrics, "Missing 'mse' key in metrics.json"
    assert "avg_inference_sec" in metrics, "Missing 'avg_inference_sec' key in metrics.json"

    assert isinstance(metrics["mse"], (int, float)), "'mse' must be a number."
    assert isinstance(metrics["avg_inference_sec"], (int, float)), "'avg_inference_sec' must be a number."
    assert metrics["mse"] > 0, "MSE should be positive."
    assert metrics["avg_inference_sec"] >= 0, "Average inference time should be non-negative."

def test_plot_script_and_image():
    script_path = "/home/user/plot_data.py"
    assert os.path.exists(script_path), "plot_data.py is missing."

    img_path = "/home/user/scatter.png"
    assert os.path.exists(img_path), "scatter.png is missing."

    with open(img_path, "rb") as f:
        header = f.read(8)
        # PNG magic bytes: \x89PNG\r\n\x1a\n
        assert header == b"\x89PNG\r\n\x1a\n", "scatter.png is not a valid PNG file."