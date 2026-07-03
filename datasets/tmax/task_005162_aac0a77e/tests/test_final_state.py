# test_final_state.py
import os
import sys
import subprocess
import random
import string
import csv
import io
import time
import urllib.request

def generate_random_csv(num_lines):
    out = io.StringIO()
    writer = csv.writer(out)
    for i in range(num_lines):
        event_id = f"evt_{i}_{random.randint(1000, 9999)}"
        timestamp = f"2023-10-10T10:00:{random.randint(10, 59)}Z"
        length = random.randint(0, 500)
        raw_text = "".join(random.choices(string.printable, k=length))
        writer.writerow([event_id, timestamp, raw_text])
    return out.getvalue()

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/reference_analyzer.py"
    agent_path = "/home/user/analyzer.py"

    assert os.path.isfile(oracle_path), f"Oracle script missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent script missing at {agent_path}"

    random.seed(42)
    for i in range(500):
        num_lines = random.randint(50, 200)
        csv_input = generate_random_csv(num_lines)

        oracle_proc = subprocess.run(
            [sys.executable, oracle_path],
            input=csv_input,
            text=True,
            capture_output=True
        )
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run(
            [sys.executable, agent_path],
            input=csv_input,
            text=True,
            capture_output=True
        )
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            assert False, (
                f"Output mismatch on random input {i}.\n"
                f"Input preview:\n{csv_input[:200]}...\n"
                f"Oracle preview:\n{oracle_out[:200]}...\n"
                f"Agent preview:\n{agent_out[:200]}..."
            )

def test_pipeline_orchestration():
    script_path = "/home/user/start_pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script missing at {script_path}"

    # Run pipeline script
    subprocess.run(["bash", script_path], check=True)
    time.sleep(2)

    # Clear Redis list first
    subprocess.run(["redis-cli", "DEL", "anomalies"], capture_output=True)

    # POST to API
    csv_data = generate_random_csv(100)
    req = urllib.request.Request(
        "http://localhost:5000/submit", 
        data=csv_data.encode('utf-8'), 
        headers={'Content-Type': 'text/plain'}
    )
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        assert False, f"Failed to POST to API server at http://localhost:5000/submit: {e}"

    time.sleep(3)

    # Check Redis
    redis_proc = subprocess.run(["redis-cli", "LRANGE", "anomalies", "0", "-1"], capture_output=True, text=True)
    lines = [line for line in redis_proc.stdout.strip().split('\n') if line]

    assert len(lines) == 100, f"Expected 100 lines in Redis 'anomalies' list, got {len(lines)}. Pipeline is not processing data correctly."