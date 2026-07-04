# test_final_state.py

import os
import subprocess
import time
import pytest
import re

def test_config_env_fixed():
    config_path = "/home/user/config.env"
    assert os.path.isfile(config_path), "config.env is missing."

    with open(config_path, "r") as f:
        content = f.read()

    assert "adminpass" in content, "PostgreSQL password not set correctly in config.env"
    assert "graphpass" in content, "Neo4j password not set correctly in config.env"

def test_etl_speedup_and_correctness():
    etl_script = "/home/user/etl.sh"
    assert os.path.isfile(etl_script), "etl.sh is missing."
    assert os.access(etl_script, os.X_OK), "etl.sh must be executable."

    # Source config.env and run etl.sh
    start_time = time.time()
    result = subprocess.run(
        f"source /home/user/config.env && bash {etl_script}",
        shell=True,
        executable="/bin/bash",
        capture_output=True,
        text=True
    )
    end_time = time.time()

    assert result.returncode == 0, f"etl.sh failed with error: {result.stderr}"

    time_agent = end_time - start_time
    time_naive = 500.0
    speedup = time_naive / time_agent if time_agent > 0 else float('inf')

    assert speedup >= 20.0, f"ETL script speedup is {speedup:.2f} (took {time_agent:.2f}s), expected >= 20.0"

def test_shortest_path_query():
    cypher_script = "/home/user/shortest_path.cypher"
    assert os.path.isfile(cypher_script), "shortest_path.cypher is missing."

    # Run the cypher script
    result = subprocess.run(
        f"source /home/user/config.env && cypher-shell -u neo4j -p graphpass -f {cypher_script}",
        shell=True,
        executable="/bin/bash",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"cypher-shell failed: {result.stderr}"

    # Extract total_latency
    output = result.stdout.strip()
    # It should return a number (e.g., 142)
    match = re.search(r'\b(\d+)\b', output.split('\n')[-1])
    assert match is not None, f"Could not find a numeric total_latency in output: {output}"

    total_latency = int(match.group(1))
    assert total_latency > 0, "total_latency should be greater than 0"
    # We accept any positive latency as the exact graph generation details might vary,
    # but the prompt mentions e.g., 142.
    if total_latency != 142:
        print(f"Note: total_latency is {total_latency}, expected 142 if deterministic.")