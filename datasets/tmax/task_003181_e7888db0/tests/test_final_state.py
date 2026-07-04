# test_final_state.py
import os
import re
import csv
import io
import random
import string
import subprocess
import pytest

def generate_csv_stream(seed, num_rows=100):
    rng = random.Random(seed)
    out = io.StringIO()
    writer = csv.writer(out, quoting=csv.QUOTE_MINIMAL)

    charset = string.ascii_letters + string.digits + string.punctuation + " \n"

    current_ts = rng.randint(1700000000, 1700000000 + 10000)
    for _ in range(num_rows):
        current_ts += rng.randint(0, 500)

        len2 = rng.randint(5, 100)
        col2 = "".join(rng.choices(charset, k=len2))

        len3 = rng.randint(5, 120)
        col3 = "".join(rng.choices(charset, k=len3))

        # Randomly force quotes even if not strictly needed
        if rng.random() < 0.3:
            # We can't easily force csv.writer to quote a specific field unless we use QUOTE_ALL
            # But we can just let csv.writer handle it.
            pass

        writer.writerow([current_ts, col2, col3])

    return out.getvalue()

def test_cron_file_exists_and_valid():
    cron_path = "/home/user/sync_cron"
    assert os.path.exists(cron_path), f"Cron file {cron_path} is missing."
    with open(cron_path, "r") as f:
        content = f.read().strip()

    regex = r"^(?:\*/15|0,15,30,45)\s+\*\s+\*\s+\*\s+\*\s+python3 /home/user/loc_etl\.py < /tmp/input\.csv > /tmp/output\.csv$"
    assert re.match(regex, content), f"Cron file content does not match expected pattern. Got: {content}"

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_loc_etl"
    agent_script = "/home/user/loc_etl.py"

    assert os.path.exists(oracle_path), f"Oracle {oracle_path} missing."
    assert os.path.exists(agent_script), f"Agent script {agent_script} missing."

    # Generate 5 different streams to test various edge cases
    for i in range(5):
        csv_input = generate_csv_stream(seed=42+i, num_rows=100)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=csv_input,
                text=True,
                capture_output=True,
                check=True,
                timeout=5
            )
            oracle_output = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            oracle_output = e.stdout

        # Run agent
        try:
            agent_proc = subprocess.run(
                ["python3", agent_script],
                input=csv_input,
                text=True,
                capture_output=True,
                check=True,
                timeout=5
            )
            agent_output = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input seed {42+i}:\n{e.stderr}")

        if oracle_output != agent_output:
            pytest.fail(
                f"Output mismatch on seed {42+i}.\n"
                f"=== INPUT (first 500 chars) ===\n{csv_input[:500]}\n"
                f"=== ORACLE OUTPUT ===\n{oracle_output}\n"
                f"=== AGENT OUTPUT ===\n{agent_output}\n"
            )