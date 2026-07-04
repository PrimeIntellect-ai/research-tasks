# test_final_state.py
import os
import subprocess
import random
import csv
import json
import tempfile
import pytest

ORACLE_PATH = "/app/legacy_pipeline"
AGENT_SCRIPT = "/home/user/clean_data.py"

def generate_users(num_rows):
    users = []
    for _ in range(num_rows):
        user_id = random.randint(10**16, 9223372036854775800)
        age = "" if random.random() < 0.10 else str(random.randint(18, 80))
        risk_score = f"{random.uniform(0.0, 1.0):.2f}"
        users.append({"user_id": str(user_id), "age": age, "risk_score": risk_score})
    return users

def generate_txns(num_rows, user_ids):
    txns = []
    for _ in range(num_rows):
        txn_id = random.randint(10**16, 9223372036854775800)
        if user_ids and random.random() < 0.8:
            user_id = random.choice(user_ids)
        else:
            user_id = str(random.randint(10**16, 9223372036854775800))

        if random.random() < 0.05:
            amount = ""
        else:
            amount = str(random.randint(-2000000, 2000000))

        status = random.choice(['COMPLETED', 'PENDING', 'FAILED'])
        txns.append({"txn_id": str(txn_id), "user_id": user_id, "amount": amount, "status": status})
    return txns

def write_csv(filepath, fieldnames, data):
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

@pytest.mark.parametrize("iteration", range(100))
def test_fuzz_equivalence(iteration):
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"

    random.seed(42 + iteration)

    num_users = random.randint(10, 1000)
    num_txns = random.randint(0, 5000)

    users_data = generate_users(num_users)
    user_ids = [u["user_id"] for u in users_data]
    txns_data = generate_txns(num_txns, user_ids)

    with tempfile.TemporaryDirectory() as tmpdir:
        users_csv = os.path.join(tmpdir, "users.csv")
        txns_csv = os.path.join(tmpdir, "txns.csv")
        track_json = os.path.join(tmpdir, "track.json")

        write_csv(users_csv, ["user_id", "age", "risk_score"], users_data)
        write_csv(txns_csv, ["txn_id", "user_id", "amount", "status"], txns_data)

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [ORACLE_PATH, users_csv, txns_csv],
                capture_output=True,
                text=True,
                check=True
            )
            oracle_out = oracle_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed: {e.stderr}")

        # Run agent
        try:
            agent_cmd = ["python3", AGENT_SCRIPT, users_csv, txns_csv]
            if iteration < 10:  # test tracking on first 10 iterations
                agent_cmd.extend(["--track", track_json])

            agent_res = subprocess.run(
                agent_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            agent_out = agent_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed: {e.stderr}")

        # Compare outputs
        assert agent_out == oracle_out, (
            f"Output mismatch on iteration {iteration}.\n"
            f"Agent output:\n{agent_out[:500]}...\n"
            f"Oracle output:\n{oracle_out[:500]}..."
        )

        if iteration < 10:
            assert os.path.exists(track_json), f"Tracking file {track_json} was not created."
            with open(track_json, 'r') as f:
                try:
                    track_data = json.load(f)
                except json.JSONDecodeError:
                    pytest.fail("Tracking file is not valid JSON.")

            assert "outliers_dropped" in track_data, "Missing 'outliers_dropped' in track JSON."
            assert "ages_imputed" in track_data, "Missing 'ages_imputed' in track JSON."

            # Simple validation, exact values would require re-implementing the logic
            # but we can check types
            assert isinstance(track_data["outliers_dropped"], int)
            assert isinstance(track_data["ages_imputed"], int)