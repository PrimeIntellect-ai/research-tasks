# test_final_state.py

import os
import sys
import json
import sqlite3
import subprocess
import tempfile
import random
import string

def test_recovered_db_exists_and_valid():
    recovered_path = "/home/user/data/recovered.db"
    assert os.path.exists(recovered_path), f"Recovered database not found at {recovered_path}"

    # Check if it's a valid SQLite DB by running a simple query
    try:
        conn = sqlite3.connect(recovered_path)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in c.fetchall()]
        conn.close()
        assert "records" in tables, f"Expected 'records' table in recovered DB, found: {tables}"
    except sqlite3.DatabaseError as e:
        pytest.fail(f"Recovered database is invalid or corrupted: {e}")

def generate_eval_db(db_path, num_rows=100000):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE records (id INTEGER PRIMARY KEY, payload TEXT)")

    rows = []
    for i in range(num_rows):
        if random.random() < 0.8:
            # Valid payload
            text = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            payload = bytes([b ^ 0x5A for b in text.encode('utf-8')]).hex()
        else:
            # Invalid payload
            if random.random() < 0.5:
                # Odd length
                payload = "12345"
            else:
                # Invalid hex
                payload = "ZZZZ"
        rows.append((i, payload))

    c.executemany("INSERT INTO records (id, payload) VALUES (?, ?)", rows)
    conn.commit()
    conn.close()

def golden_processor(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, payload FROM records")
    results = {}
    for row_id, payload in c:
        try:
            if len(payload) % 2 != 0:
                continue
            bytes_data = bytes.fromhex(payload)
            transformed = bytes([b ^ 0x5A for b in bytes_data]).decode('utf-8')
            results[str(row_id)] = transformed
        except Exception:
            continue
    conn.close()
    return results

def test_safe_processor_accuracy_and_memory():
    script_path = "/home/user/safe_processor.py"
    assert os.path.exists(script_path), f"Expected script not found at {script_path}"

    # Generate hidden evaluation DB
    eval_db_path = "/tmp/eval.db"
    out_json_path = "/tmp/out.json"
    if os.path.exists(eval_db_path):
        os.remove(eval_db_path)
    if os.path.exists(out_json_path):
        os.remove(out_json_path)

    generate_eval_db(eval_db_path, num_rows=100000)

    # Run the agent's script with time -v to measure memory
    cmd = ["/usr/bin/time", "-v", sys.executable, script_path, eval_db_path, out_json_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    # Parse memory usage
    max_memory_kb = None
    for line in result.stderr.splitlines():
        if "Maximum resident set size (kbytes):" in line:
            max_memory_kb = int(line.split(":")[1].strip())
            break

    assert max_memory_kb is not None, "Could not parse memory usage from /usr/bin/time output"
    max_memory_mb = max_memory_kb / 1024.0

    # Check memory limit
    assert max_memory_mb <= 50.0, f"Memory limit exceeded: {max_memory_mb:.2f} MB > 50.0 MB"

    # Check accuracy
    assert os.path.exists(out_json_path), "Output JSON file was not created"
    with open(out_json_path, 'r') as f:
        try:
            agent_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output JSON is invalid")

    # Convert keys to string for comparison since JSON keys are strings
    golden_results = golden_processor(eval_db_path)

    # Compare
    assert len(agent_results) == len(golden_results), f"Result count mismatch. Expected {len(golden_results)}, got {len(agent_results)}"

    for k, v in golden_results.items():
        assert k in agent_results, f"Missing key {k} in output"
        assert agent_results[k] == v, f"Value mismatch for key {k}. Expected {v}, got {agent_results[k]}"