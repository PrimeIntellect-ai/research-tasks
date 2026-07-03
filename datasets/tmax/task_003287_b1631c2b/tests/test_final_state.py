# test_final_state.py

import os
import subprocess
import socket
import threading
import time
import random
import pytest

ORACLE_PATH = "/opt/oracle/log_aggregator_oracle"
AGENT_PATH = "/home/user/app/log_aggregator_fixed"
REDIS_PORT = "6379"

def check_executable(path):
    assert os.path.isfile(path), f"Executable not found: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def get_redis_val(key):
    try:
        out = subprocess.check_output(["redis-cli", "-p", REDIS_PORT, "GET", key]).decode().strip()
        if out == "(nil)" or out == "":
            return None
        return float(out)
    except Exception:
        return None

def clear_redis():
    subprocess.check_call(["redis-cli", "-p", REDIS_PORT, "FLUSHALL"])

def generate_log_lines(num_lines):
    lines = []
    for _ in range(num_lines):
        if random.random() < 0.05:
            # malformed
            lines.append("MALFORMED LINE " + str(random.random()))
            continue

        timestamp = f"[{random.randint(1000000000, 1999999999)}]"
        event_id = f"EVT_{random.randint(1, 100)}"

        fmt_choice = random.choice(["normal", "e-", "e+"])
        if fmt_choice == "normal":
            val = round(random.uniform(-1000.0, 1000.0), 4)
            val_str = str(val)
        elif fmt_choice == "e-":
            val = random.uniform(1.0, 9.9)
            exp = random.randint(1, 20)
            val_str = f"{val}e-{exp}"
        else:
            val = random.uniform(1.0, 9.9)
            exp = random.randint(1, 20)
            val_str = f"{val}E+{exp}"

        spaces = " " * random.randint(1, 3)
        line = f"{timestamp}{spaces}{event_id}{spaces}{val_str}"
        lines.append(line)
    return lines

def serve_data_and_run(executable, lines, port):
    clear_redis()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', port))
    server.listen(1)

    def handle_client():
        try:
            server.settimeout(5.0)
            conn, addr = server.accept()
            data_str = "\n".join(lines) + "\n"
            conn.sendall(data_str.encode('utf-8'))
            time.sleep(0.5) # Give it time to process before closing
            conn.close()
        except Exception:
            pass
        finally:
            server.close()

    t = threading.Thread(target=handle_client)
    t.start()

    proc = subprocess.Popen([executable, str(port), REDIS_PORT])
    t.join(timeout=6.0)

    # Wait a bit for the process to finish writing to Redis
    time.sleep(0.5)

    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=2.0)
        except subprocess.TimeoutExpired:
            proc.kill()

    s = get_redis_val("sum_values")
    c = get_redis_val("count_events")
    return s, c

def test_fuzz_equivalence():
    check_executable(ORACLE_PATH)
    check_executable(AGENT_PATH)

    random.seed(42)
    N_RUNS = 20 # Reduced from 50 for test execution time, but sufficient for fuzzing
    LINES_PER_RUN = 1000

    port = 18080

    for run in range(N_RUNS):
        lines = generate_log_lines(LINES_PER_RUN)

        oracle_sum, oracle_count = serve_data_and_run(ORACLE_PATH, lines, port)
        agent_sum, agent_count = serve_data_and_run(AGENT_PATH, lines, port)

        assert oracle_count is not None, "Oracle failed to write count_events to Redis."
        assert agent_count is not None, "Agent failed to write count_events to Redis."

        assert agent_count == oracle_count, f"Run {run}: count_events mismatch. Oracle: {oracle_count}, Agent: {agent_count}"

        if oracle_sum is not None and agent_sum is not None:
            # Compare floats with a small tolerance due to potential precision differences
            assert abs(agent_sum - oracle_sum) < 1e-4, f"Run {run}: sum_values mismatch. Oracle: {oracle_sum}, Agent: {agent_sum}"
        else:
            assert agent_sum == oracle_sum, f"Run {run}: sum_values mismatch. Oracle: {oracle_sum}, Agent: {agent_sum}"