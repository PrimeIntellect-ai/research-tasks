# test_final_state.py

import os
import subprocess
import pytest

def test_dataset_exists():
    assert os.path.exists("/home/user/workspace/dataset.csv"), "dataset.csv not found in /home/user/workspace/"

def test_dataset_format_and_accuracy():
    agent_file = "/home/user/workspace/dataset.csv"
    assert os.path.exists(agent_file), "dataset.csv not found."

    # Compute reference data using awk to ensure identical PRNG sequence
    reference_data = {}
    for seed in range(1000, 1100):
        awk_cmd = f"awk -v s={seed} 'BEGIN {{ for(i=1; i<=500; i++) {{ srand(s+i); printf \"%.6f\\n\", rand() * 100 }} }}'"
        proc = subprocess.run(awk_cmd, shell=True, capture_output=True, text=True)
        vals = [float(x) for x in proc.stdout.strip().split("\n")]

        ema = None
        for val in vals:
            if ema is None:
                ema = val
            else:
                ema = 0.1 * val + 0.9 * ema

        reference_data[seed] = ema

    max_err = 0.0
    agent_count = 0
    previous_seed = -1

    with open(agent_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            parts = line.split(",")
            assert len(parts) == 2, f"Invalid format in line: '{line}'. Expected 'seed,val'"
            seed_str, val_str = parts
            try:
                seed = int(seed_str)
                val = float(val_str)
            except ValueError:
                pytest.fail(f"Could not parse numerical values from line: '{line}'")

            assert seed > previous_seed, f"Seeds are not sorted numerically. Found {seed} after {previous_seed}"
            previous_seed = seed

            if seed in reference_data:
                err = abs(reference_data[seed] - val)
                max_err = max(max_err, err)
                agent_count += 1
            else:
                pytest.fail(f"Unexpected seed {seed} found in dataset.")

    assert agent_count == 100, f"Expected exactly 100 seeds, found {agent_count}."
    assert max_err <= 1e-4, f"Max Absolute Error exceeds tolerance. Max err: {max_err} > 1e-4"