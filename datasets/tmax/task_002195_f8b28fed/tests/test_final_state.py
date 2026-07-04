# test_final_state.py

import os
import csv
import math

def test_best_run_computation():
    artifacts_path = "/home/user/artifacts.csv"
    embeddings_path = "/home/user/embeddings.tsv"
    output_path = "/home/user/best_run.txt"
    script_path = "/home/user/find_best_run.sh"

    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.path.isfile(output_path), f"Output file not found at {output_path}"

    # 1. Parse artifacts and calculate efficiency
    efficiencies = []
    with open(artifacts_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            run_id = row['run_id']
            accuracy = float(row['accuracy'])
            training_time = float(row['training_time'])
            efficiency = accuracy / training_time
            efficiencies.append((run_id, efficiency))

    # 2. Identify top 5 runs by efficiency
    # Sort descending by efficiency
    efficiencies.sort(key=lambda x: x[1], reverse=True)
    top_5_runs = {x[0] for x in efficiencies[:5]}

    # 3. Parse embeddings and calculate dot products for top 5
    query_vector = [0.1, 0.5, 0.2, -0.1, 0.8]
    best_run_id = None
    max_dot_product = -float('inf')

    with open(embeddings_path, 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if not parts or len(parts) < 6:
                continue
            run_id = parts[0]
            if run_id in top_5_runs:
                vector = [float(x) for x in parts[1:6]]
                dot_product = sum(a * b for a, b in zip(vector, query_vector))
                if dot_product > max_dot_product:
                    max_dot_product = dot_product
                    best_run_id = run_id

    # Read the actual output
    with open(output_path, 'r') as f:
        actual_output = f.read().strip()

    # Parse actual output
    parts = actual_output.split(',')
    assert len(parts) == 2, f"Output in {output_path} must be in format 'run_id,dot_product', got '{actual_output}'"
    actual_run_id = parts[0].strip()
    actual_dot_product = float(parts[1].strip())

    # Assertions
    assert actual_run_id == best_run_id, f"Expected best run_id '{best_run_id}', but got '{actual_run_id}'"
    assert math.isclose(actual_dot_product, max_dot_product, rel_tol=1e-5, abs_tol=1e-5), \
        f"Expected dot product {max_dot_product}, but got {actual_dot_product}"