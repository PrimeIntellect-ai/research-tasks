# test_final_state.py
import os
import re
from collections import defaultdict, deque

def test_files_exist():
    assert os.path.isfile("/home/user/analyze.cpp"), "/home/user/analyze.cpp is missing."
    assert os.path.isfile("/home/user/analyze"), "/home/user/analyze executable is missing. Did you compile it?"
    assert os.path.isfile("/home/user/alerts.txt"), "/home/user/alerts.txt is missing. Did you run the program?"

def test_alerts_content():
    log_file = "/home/user/server.log"
    assert os.path.isfile(log_file), f"The file {log_file} is missing."

    windows = defaultdict(lambda: deque(maxlen=3))
    expected_alerts = []

    # regex to parse log line: [date] METHOD ENDPOINT LATENCY
    pattern = re.compile(r'^\[.*?\]\s+\S+\s+(\S+)\s+(\d+)$')

    with open(log_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if match:
                endpoint = match.group(1)
                latency = int(match.group(2))

                windows[endpoint].append(latency)
                if len(windows[endpoint]) == 3:
                    avg = sum(windows[endpoint]) // 3
                    if avg >= 500:
                        expected_alerts.append(
                            f"ALERT: {endpoint} is experiencing degradation. Current 3-request rolling average is {avg}ms."
                        )

    alerts_file = "/home/user/alerts.txt"
    with open(alerts_file, 'r') as f:
        actual_alerts = [line.strip() for line in f if line.strip()]

    assert actual_alerts == expected_alerts, (
        f"Contents of {alerts_file} do not match the expected alerts.\n"
        f"Expected:\n" + "\n".join(expected_alerts) + "\n\n"
        f"Actual:\n" + "\n".join(actual_alerts)
    )