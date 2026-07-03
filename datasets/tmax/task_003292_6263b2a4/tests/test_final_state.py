# test_final_state.py
import os
import json
import pytest

def test_recovered_logs_exist_and_valid():
    log_path = "/home/user/recovered_logs.jsonl"
    assert os.path.isfile(log_path), f"Recovered logs file missing at {log_path}"

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 100, f"Expected 100 log entries, found {len(lines)}"

    for i, line in enumerate(lines):
        try:
            parsed = json.loads(line)
            assert "timestamp" in parsed, f"Line {i} missing 'timestamp' field"
            assert "sensor_val" in parsed, f"Line {i} missing 'sensor_val' field"
        except json.JSONDecodeError:
            pytest.fail(f"Line {i} is not valid JSON: {line}")

def test_metrics_json_correctness():
    metrics_path = "/home/user/metrics.json"
    assert os.path.isfile(metrics_path), f"Metrics file missing at {metrics_path}"

    with open(metrics_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Metrics file at {metrics_path} is not valid JSON")

    assert "processed_count" in metrics, "Metrics JSON missing 'processed_count'"
    assert metrics["processed_count"] == 100, f"Expected processed_count to be 100, got {metrics['processed_count']}"

    assert "total_sensor_value" in metrics, "Metrics JSON missing 'total_sensor_value'"

    # Calculate the exact expected value
    # 100 entries: val = 100000.0 + (i * 0.125)
    # Sum = 100 * 100000.0 + sum(i * 0.125 for i in range(100))
    # Sum = 10000000.0 + (99 * 100 / 2) * 0.125 = 10000000.0 + 4950 * 0.125 = 10000618.75
    expected_total = 10000618.75

    actual_total = metrics["total_sensor_value"]
    assert actual_total == expected_total, f"Expected total_sensor_value to be exactly {expected_total}, got {actual_total}. Check if f64 was used for accumulation."

def test_rust_code_fixes():
    main_rs_path = "/home/user/log_processor/src/main.rs"
    assert os.path.isfile(main_rs_path), f"Rust source file missing at {main_rs_path}"

    with open(main_rs_path, "r") as f:
        content = f.read()

    # The off-by-one bug should be fixed (no <= entries.len())
    assert "i <= entries.len()" not in content, "The off-by-one error (<= entries.len()) is still present in main.rs"

    # The precision bug should be fixed (f32 replaced by f64 for total)
    assert "total: f32" not in content, "The precision loss bug (total: f32) is still present in main.rs"
    assert "as f32" not in content, "Casting to f32 is still present in main.rs"