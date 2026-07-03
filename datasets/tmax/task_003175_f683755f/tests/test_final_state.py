# test_final_state.py
import json
import math
import os

def test_summary_json_exists_and_correct():
    summary_path = "/home/user/summary.json"
    metrics_path = "/home/user/metrics.jsonl"

    assert os.path.exists(summary_path), f"File {summary_path} is missing. The Go script must generate this file."
    assert os.path.exists(metrics_path), f"File {metrics_path} is missing."

    valid_count = 0
    selected_latencies = []

    # Derive expected state from input file
    with open(metrics_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Schema validation
            if not all(k in data for k in ("model_id", "features", "latency_ms")):
                continue
            if not isinstance(data["model_id"], str):
                continue
            if not isinstance(data["features"], list) or len(data["features"]) != 3:
                continue

            try:
                features = [float(x) for x in data["features"]]
            except (ValueError, TypeError):
                continue

            if not isinstance(data["latency_ms"], (int, float)) or isinstance(data["latency_ms"], bool):
                continue

            valid_count += 1

            # Feature Selection
            l2_norm = math.sqrt(sum(x*x for x in features))
            if l2_norm >= 10.0:
                selected_latencies.append(float(data["latency_ms"]))

    selected_count = len(selected_latencies)

    # P95 Calculation
    selected_latencies.sort()
    if selected_count > 0:
        idx = int(math.ceil(0.95 * selected_count)) - 1
        expected_p95 = selected_latencies[idx]
    else:
        expected_p95 = 0.0

    # Validate final output
    with open(summary_path, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {summary_path} is not valid JSON."

    assert "valid_records" in summary, "Missing 'valid_records' in summary.json"
    assert "selected_records" in summary, "Missing 'selected_records' in summary.json"
    assert "p95_latency" in summary, "Missing 'p95_latency' in summary.json"

    assert summary["valid_records"] == valid_count, f"Expected {valid_count} valid_records, got {summary['valid_records']}"
    assert summary["selected_records"] == selected_count, f"Expected {selected_count} selected_records, got {summary['selected_records']}"
    assert math.isclose(summary["p95_latency"], expected_p95, rel_tol=1e-5), f"Expected p95_latency ~{expected_p95}, got {summary['p95_latency']}"