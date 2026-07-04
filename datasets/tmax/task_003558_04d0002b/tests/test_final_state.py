# test_final_state.py
import os
import time
import string
import random
import subprocess
import urllib.request
import urllib.error

def test_nginx_proxy_working():
    """Test that Nginx correctly proxies requests to the backend API."""
    url = "http://127.0.0.1:8080/api/metrics"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except urllib.error.URLError as e:
        assert False, f"Failed to reach Nginx on 127.0.0.1:8080 or proxy failed: {e}"

def test_backup_job():
    """Test that the cron backup job properly copies the database file."""
    data_file = "/home/user/data/metrics.db"
    backup_file = "/home/user/metrics_backup/metrics.db.bak"

    # Write unique data to the source file
    unique_data = os.urandom(16)
    with open(data_file, "wb") as f:
        f.write(unique_data)

    # Wait for up to 65 seconds for the backup file to match
    matched = False
    for _ in range(70):
        if os.path.exists(backup_file):
            try:
                with open(backup_file, "rb") as f:
                    if f.read() == unique_data:
                        matched = True
                        break
            except Exception:
                pass
        time.sleep(1)

    assert matched, "Backup job failed to copy the file correctly to /home/user/metrics_backup/metrics.db.bak within 65 seconds. Check cron and script paths."

def generate_fuzz_inputs():
    """Generate 1000 lines of fuzz input according to the distribution."""
    random.seed(42)
    inputs = []

    # 400 valid lines
    for _ in range(400):
        ts = f"[{random.randint(2000,2025):04d}-{random.randint(1,12):02d}-{random.randint(1,28):02d}T{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}Z]"
        metric = "".join(random.choices(string.ascii_letters + string.digits + "_", k=random.randint(3, 10)))
        val = random.uniform(0, 100)
        num_tags = random.randint(1, 5)
        tags = ",".join("".join(random.choices(string.ascii_letters, k=4)) for _ in range(num_tags))
        inputs.append(f"{ts} {metric}: {val:.4f} tags={tags}")

    # 200 missing fields
    for _ in range(200):
        ts = f"[{random.randint(2000,2025):04d}-{random.randint(1,12):02d}-{random.randint(1,28):02d}T00:00:00Z]"
        metric = "metric_name"
        inputs.append(random.choice([
            f"{metric}: 1.0 tags=a,b",  # missing ts
            f"{ts} 1.0 tags=a,b",       # missing metric
            f"{ts} {metric}: tags=a,b", # missing value
            f"{ts} {metric}: 1.0"       # missing tags
        ]))

    # 200 invalid float formats or mismatched delimiters
    for _ in range(200):
        ts = "[2023-01-01T00:00:00Z]"
        inputs.append(random.choice([
            f"{ts} metric: notafloat tags=a,b",
            f"{ts} metric 1.0 tags=a,b", # missing colon
            f"2023-01-01T00:00:00Z metric: 1.0 tags=a,b" # missing brackets
        ]))

    # 200 completely random alphanumeric strings
    for _ in range(200):
        inputs.append("".join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 100))))

    random.shuffle(inputs)
    return "\n".join(inputs) + "\n"

def test_normalizer_fuzz_equivalence():
    """Fuzz test the normalizer script against the oracle binary."""
    oracle_path = "/app/oracle_normalizer"
    agent_path = "/home/user/normalizer.py"

    assert os.path.exists(agent_path), f"Agent script not found at {agent_path}"
    assert os.path.exists(oracle_path), f"Oracle binary not found at {oracle_path}"

    inputs = generate_fuzz_inputs()

    oracle_proc = subprocess.run([oracle_path], input=inputs, text=True, capture_output=True)
    agent_proc = subprocess.run(["python3", agent_path], input=inputs, text=True, capture_output=True)

    oracle_out = oracle_proc.stdout.splitlines()
    agent_out = agent_proc.stdout.splitlines()

    input_lines = inputs.splitlines()

    assert len(agent_out) == len(oracle_out), f"Output line count mismatch: Oracle produced {len(oracle_out)} lines, Agent produced {len(agent_out)} lines."

    for i, (o_line, a_line) in enumerate(zip(oracle_out, agent_out)):
        assert o_line == a_line, (
            f"Mismatch on input line {i + 1}:\n"
            f"Input:  {input_lines[i]}\n"
            f"Oracle: {o_line}\n"
            f"Agent:  {a_line}"
        )