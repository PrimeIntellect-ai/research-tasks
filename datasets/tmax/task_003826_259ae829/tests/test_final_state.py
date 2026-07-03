# test_final_state.py

import os
import socket
import threading
import time
import requests

def test_poison_pill_extracted():
    path = "/home/user/poison_pill.txt"
    assert os.path.exists(path), f"File {path} does not exist. You must extract the poison pill."
    with open(path, "r") as f:
        content = f.read().strip()
    assert "POISON_PILL_ERR_DEADBEEF_90210" in content, f"Incorrect poison pill extracted. Found: {content}"

def test_concurrent_ingestion_and_aggregation():
    device_id = "DEV_TEST_CONCURRENT"
    num_threads = 10
    metrics_per_thread = 100
    metric_value = 1

    errors = []

    def send_metrics():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect(("127.0.0.1", 8080))
            for _ in range(metrics_per_thread):
                msg = f"SECRET_AUTH_99:{device_id}:{metric_value}\n"
                s.sendall(msg.encode("utf-8"))
                time.sleep(0.001)  # slightly interleave to encourage race conditions
            s.close()
        except Exception as e:
            errors.append(e)

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=send_metrics)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert not errors, f"Errors occurred during concurrent ingestion: {errors}"

    # Allow a brief moment for the aggregator to finish processing and writing to Redis
    time.sleep(1)

    # Query the Python dashboard
    try:
        resp = requests.get("http://127.0.0.1:9000/api/stats", timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to dashboard on port 9000: {e}"

    assert resp.status_code == 200, f"Dashboard returned HTTP {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        assert False, f"Dashboard did not return valid JSON. Response: {resp.text}"

    assert device_id in data, f"Device {device_id} not found in aggregated stats. Is the aggregator dropping data? Got: {data}"

    stats = data[device_id]
    expected_count = num_threads * metrics_per_thread
    expected_sum = expected_count * metric_value

    assert stats.get("count") == expected_count, f"Expected count {expected_count}, got {stats.get('count')}. Deadlock or race condition may still exist."
    assert stats.get("sum") == expected_sum, f"Expected sum {expected_sum}, got {stats.get('sum')}. Deadlock or race condition may still exist."