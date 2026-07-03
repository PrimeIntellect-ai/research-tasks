# test_final_state.py

import os
import subprocess
import json
import struct
import random
import pytest

def test_rust_binary_matches_legacy():
    rust_bin = "/home/user/sensor_aggregator/target/release/sensor_aggregator"
    assert os.path.exists(rust_bin), f"Rust binary not found at {rust_bin}. Did you run 'cargo build --release'?"

    legacy_bin = "/app/legacy_calc"
    assert os.path.exists(legacy_bin), f"Legacy binary missing at {legacy_bin}"

    test_file = "/tmp/test_data.bin"

    # Generate test data: 500,000 records to expose concurrency and precision issues
    random.seed(42)
    with open(test_file, 'wb') as f:
        for _ in range(500000):
            sensor_id = random.randint(1, 50)
            reading = random.uniform(-10000.0, 10000.0)
            f.write(struct.pack('<Id', sensor_id, reading))

    # Run legacy binary
    try:
        with open(test_file, 'rb') as f:
            legacy_proc = subprocess.run(
                [legacy_bin], 
                stdin=f, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True, 
                check=True
            )
        legacy_out = json.loads(legacy_proc.stdout)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Legacy binary failed to run: {e.stderr}")
    except json.JSONDecodeError:
        pytest.fail("Legacy binary did not output valid JSON.")

    # Run rust binary
    try:
        rust_proc = subprocess.run(
            [rust_bin, test_file], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True, 
            check=True
        )
        rust_out = json.loads(rust_proc.stdout)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Rust binary failed to run: {e.stderr}")
    except json.JSONDecodeError:
        pytest.fail("Rust binary did not output valid JSON.")

    # Calculate MAE
    mae = 0.0
    for k in legacy_out.keys():
        ref_val = legacy_out[k]
        # Handle string keys since JSON keys are strings
        hyp_val = rust_out.get(k, 0.0)
        mae = max(mae, abs(ref_val - hyp_val))

    # Also check if rust output has extra keys
    for k in rust_out.keys():
        if k not in legacy_out:
            ref_val = 0.0
            hyp_val = rust_out[k]
            mae = max(mae, abs(ref_val - hyp_val))

    threshold = 1e-8
    assert mae < threshold, f"Maximum Absolute Error {mae} is >= {threshold}. The Rust implementation's output does not match the legacy binary closely enough."