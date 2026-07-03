# test_final_state.py

import os
import json
import glob
from collections import defaultdict
import pytest

def compute_expected_ema():
    """Derive the expected EMA values from the raw logs based on the schema and formula."""
    records = []
    for fpath in glob.glob('/home/user/raw_logs/*.jsonl'):
        with open(fpath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    exp_id = data.get("experiment_id")
                    epoch = data.get("epoch")
                    val_loss = data.get("val_loss")

                    # Schema enforcement
                    if not isinstance(exp_id, str):
                        continue
                    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
                        continue

                    try:
                        val_loss = float(val_loss)
                    except (ValueError, TypeError):
                        continue

                    import math
                    if math.isnan(val_loss) or val_loss <= 0:
                        continue

                    records.append((exp_id, epoch, val_loss))
                except Exception:
                    pass

    # Group by experiment_id
    grouped = defaultdict(list)
    for exp_id, epoch, val_loss in records:
        grouped[exp_id].append((epoch, val_loss))

    emas = {}
    for exp_id, items in grouped.items():
        # Sort strictly by epoch in ascending order
        items.sort(key=lambda x: x[0])

        # Calculate EMA
        ema = items[0][1]
        for epoch, val_loss in items[1:]:
            ema = 0.2 * val_loss + 0.8 * ema
        emas[exp_id] = round(ema, 4)

    return emas

def test_summary_json_exists_and_correct():
    summary_path = '/home/user/artifacts/summary.json'
    assert os.path.exists(summary_path), f"Output file {summary_path} does not exist."
    assert os.path.isfile(summary_path), f"Path {summary_path} is not a file."

    with open(summary_path, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} does not contain valid JSON.")

    expected_data = compute_expected_ema()

    for exp_id, expected_ema in expected_data.items():
        assert exp_id in actual_data, f"Experiment {exp_id} is missing from the output."
        actual_ema = actual_data[exp_id]

        # Check that it's rounded to 4 decimal places or at least numerically equivalent
        assert abs(actual_ema - expected_ema) < 1e-4, \
            f"EMA for {exp_id} is incorrect. Expected ~{expected_ema}, got {actual_ema}."

def test_scripts_exist_and_executable():
    pipeline_script = '/home/user/run_pipeline.sh'
    process_script = '/home/user/process_metrics.py'

    assert os.path.exists(pipeline_script), f"Bash script {pipeline_script} does not exist."
    assert os.access(pipeline_script, os.X_OK), f"Bash script {pipeline_script} is not executable."

    assert os.path.exists(process_script), f"Python script {process_script} does not exist."