# test_final_state.py

import os
import time
import subprocess
import pandas as pd
import pytest

def test_fast_etl_performance_and_accuracy():
    script_path = "/home/user/fast_etl.sh"
    output_path = "/home/user/top_sources.txt"
    raw_data_path = "/home/user/data/raw_edges.csv"

    assert os.path.isfile(script_path), f"Missing script at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

    # Remove output if it exists to ensure we measure the new run
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run the script and measure wall-clock time
    start_time = time.time()
    result = subprocess.run([script_path], capture_output=True, text=True)
    end_time = time.time()

    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStderr: {result.stderr}"

    runtime = end_time - start_time
    assert runtime <= 2.0, f"Runtime {runtime:.2f}s exceeded the stringent threshold of 2.0s"

    assert os.path.isfile(output_path), f"Output file {output_path} was not created"

    # Compute golden truth
    df = pd.read_csv(raw_data_path, names=['source_ip', 'destination_ip', 'timestamp', 'bytes_transferred'])

    # 1. Filter out bytes < 100
    df = df[df['bytes_transferred'] >= 100]

    # 2. Sort by source_ip and timestamp (ascending)
    df = df.sort_values(by=['source_ip', 'timestamp'], ascending=[True, True])

    # 3. Keep exactly the 10 most recent per source_ip
    df = df.groupby('source_ip').tail(10)

    # 4. Compute score
    df['score'] = (df['bytes_transferred'] % 1000) * 1.5

    # 5. Aggregate
    agg = df.groupby('source_ip')['score'].sum().reset_index()

    # Sort descending by score to get top 25
    golden_top_25 = agg.sort_values(by=['score', 'source_ip'], ascending=[False, True]).head(25)

    # Read student output
    try:
        student_output = pd.read_csv(output_path, names=['source_ip', 'score'])
    except Exception as e:
        pytest.fail(f"Could not parse {output_path} as CSV: {e}")

    assert len(student_output) == 25, f"Expected exactly 25 lines in output, got {len(student_output)}"

    # Compare correctness
    golden_scores = golden_top_25['score'].tolist()
    student_scores = student_output['score'].tolist()

    # Check if the scores match (allowing for minor float formatting differences)
    for i, (g_score, s_score) in enumerate(zip(golden_scores, student_scores)):
        assert abs(g_score - s_score) < 1e-5, f"Rank {i+1} score mismatch: expected {g_score}, got {s_score}"

    # Check if the IPs match the expected top IPs (checking the set to avoid strict tie-breaking order issues)
    golden_ips = set(golden_top_25['source_ip'])
    student_ips = set(student_output['source_ip'])

    missing_ips = golden_ips - student_ips
    assert not missing_ips, f"Student output is missing expected top IPs: {missing_ips}"

    # Also verify that the scores associated with the IPs in the student output are correct
    golden_dict = dict(zip(agg['source_ip'], agg['score']))
    for _, row in student_output.iterrows():
        ip = row['source_ip']
        score = row['score']
        expected_score = golden_dict.get(ip)
        assert expected_score is not None, f"IP {ip} not found in valid aggregated results"
        assert abs(expected_score - score) < 1e-5, f"Incorrect score for IP {ip}: expected {expected_score}, got {score}"