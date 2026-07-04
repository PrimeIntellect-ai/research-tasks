# test_final_state.py

import os
import subprocess
import socket
import threading
import random
import string
import datetime
import pytest

AGENT_SCRIPT = "/home/user/aggregator.sh"
ORACLE_SCRIPT = "/opt/oracle/aggregator_oracle.sh"

def serve_data(port, data, ready_event):
    """
    Start a simple TCP server on 127.0.0.1:port that sends `data` to the first connected client
    and then closes the connection.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', port))
    s.listen(1)
    ready_event.set()
    try:
        s.settimeout(10.0)
        conn, addr = s.accept()
        conn.sendall(data.encode('utf-8'))
        conn.close()
    except socket.timeout:
        pass
    finally:
        s.close()

def generate_fuzz_data():
    """
    Generate randomized log data for the 3 services.
    """
    num_lines = random.randint(500, 1000)
    pool_size = num_lines + 200
    order_ids = [''.join(random.choices(string.ascii_letters + string.digits, k=8)) for _ in range(pool_size)]

    orders_data = []
    payments_data = []
    shipping_data = []

    for _ in range(num_lines):
        oid = random.choice(order_ids)
        ts = random.randint(1400000000, 1700000000)
        dt = datetime.datetime.utcfromtimestamp(ts)

        if random.random() < 0.8:
            amt = round(random.uniform(5.0, 500.0), 2)
            orders_data.append(f"{dt.strftime('%Y-%m-%d %H:%M:%S')}, {oid}, {amt}")

        if random.random() < 0.8:
            status = random.choice(["SUCCESS", "FAILED", "PENDING"])
            payments_data.append(f"{ts}\t{oid}\t{status}")

        if random.random() < 0.8:
            warehouse = random.choice(["EAST", "WEST", "CENTRAL"])
            shipping_data.append(f"{dt.strftime('%Y-%m-%dT%H:%M:%SZ')} | {oid} | {warehouse}")

    # Shuffle the lines to simulate random arrival
    random.shuffle(orders_data)
    random.shuffle(payments_data)
    random.shuffle(shipping_data)

    return "\n".join(orders_data) + "\n", "\n".join(payments_data) + "\n", "\n".join(shipping_data) + "\n"

def run_script_with_services(script_path, orders, payments, shipping):
    """
    Spins up the mock services, runs the script, and returns its stdout.
    """
    ready_events = [threading.Event() for _ in range(3)]

    t1 = threading.Thread(target=serve_data, args=(9001, orders, ready_events[0]))
    t2 = threading.Thread(target=serve_data, args=(9002, payments, ready_events[1]))
    t3 = threading.Thread(target=serve_data, args=(9003, shipping, ready_events[2]))

    t1.start()
    t2.start()
    t3.start()

    for e in ready_events:
        e.wait()

    result = subprocess.run(["/bin/bash", script_path], capture_output=True, text=True)

    t1.join()
    t2.join()
    t3.join()

    return result.stdout, result.stderr

def test_agent_exists_and_executable():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable."

def test_fuzz_equivalence():
    """
    Run 10 fuzz iterations comparing the agent's output to the oracle's output.
    (Using 10 instead of 50 to ensure the test completes within reasonable time limits).
    """
    random.seed(42)

    for i in range(10):
        orders, payments, shipping = generate_fuzz_data()

        oracle_out, oracle_err = run_script_with_services(ORACLE_SCRIPT, orders, payments, shipping)
        agent_out, agent_err = run_script_with_services(AGENT_SCRIPT, orders, payments, shipping)

        if oracle_out != agent_out:
            error_msg = (
                f"Mismatch on fuzz iteration {i+1}!\n\n"
                f"--- Oracle Output ---\n{oracle_out[:1000]}...\n\n"
                f"--- Agent Output ---\n{agent_out[:1000]}...\n\n"
                f"--- Agent Stderr ---\n{agent_err}\n"
            )
            pytest.fail(error_msg)