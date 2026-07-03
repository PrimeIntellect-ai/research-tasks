# test_final_state.py

import os
import json
import random
import subprocess
import pytest
import csv

def test_query_engine_fuzz_equivalence():
    agent_file = "/home/user/query_engine.go"
    oracle_file = "/app/bin/reference_oracle"
    csv_file = "/app/data/export.csv"

    assert os.path.isfile(agent_file), f"Missing agent file: {agent_file}"
    assert os.path.isfile(oracle_file), f"Missing oracle file: {oracle_file}"

    # Extract event IDs from CSV to form the pool of valid and invalid IDs
    event_ids = []
    if os.path.isfile(csv_file):
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "event_id" in row:
                    event_ids.append(row["event_id"])
    event_ids = list(set(event_ids))
    if not event_ids:
        # Fallback if CSV is empty or missing
        event_ids = ["10001", "10005", "10012", "10015", "10022", "10030", "99999"]

    random.seed(42)

    for i in range(500):
        num_queries = random.randint(1, 100)
        queries = []
        for _ in range(num_queries):
            queries.append({
                "type": "ancestors",
                "event_id": random.choice(event_ids),
                "limit": random.randint(1, 50),
                "sort": random.choice(["asc", "desc"])
            })

        input_json = json.dumps(queries)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_file, input_json],
            capture_output=True,
            text=True
        )

        # Run agent
        agent_proc = subprocess.run(
            ["go", "run", agent_file, input_json],
            capture_output=True,
            text=True
        )

        # We only strictly compare stdout if the oracle succeeded, but we also expect the agent to not crash unexpectedly.
        if oracle_proc.returncode == 0:
            assert agent_proc.returncode == 0, f"Agent failed but oracle succeeded on input: {input_json}\nAgent stderr: {agent_proc.stderr}"

            try:
                oracle_out = json.loads(oracle_proc.stdout)
            except json.JSONDecodeError:
                oracle_out = oracle_proc.stdout.strip()

            try:
                agent_out = json.loads(agent_proc.stdout)
            except json.JSONDecodeError:
                agent_out = agent_proc.stdout.strip()

            assert agent_out == oracle_out, f"Output mismatch on input: {input_json}\nOracle: {oracle_out}\nAgent: {agent_out}"