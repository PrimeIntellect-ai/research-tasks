# test_final_state.py

import os
import pytest
import requests

def test_server_response():
    log_file = "/app/logs/microservice.log"
    template_file = "/app/templates/report.html.tmpl"

    assert os.path.exists(log_file), f"Log file {log_file} is missing"
    assert os.path.exists(template_file), f"Template file {template_file} is missing"

    errors = []
    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            parts = line.split()
            if len(parts) >= 3:
                ts = int(parts[0])
                ip = parts[1]
                status = int(parts[2])
                if status >= 500:
                    errors.append((ts, ip))

    # Ensure errors are sorted by timestamp to evaluate rolling windows correctly
    errors.sort(key=lambda x: x[0])

    max_count = 0
    peak_time = 0
    sampled_ips = []

    # Evaluate a 60-second window ending at each error's timestamp
    for i in range(len(errors)):
        end_ts = errors[i][0]
        start_ts = end_ts - 59

        window_errors = [e for e in errors if start_ts <= e[0] <= end_ts]
        count = len(window_errors)

        if count >= 10:
            if count > max_count or (count == max_count and end_ts > peak_time):
                max_count = count
                peak_time = end_ts
                ips = []
                for e in window_errors:
                    if e[1] not in ips:
                        ips.append(e[1])
                        if len(ips) == 3:
                            break
                sampled_ips = ips

    with open(template_file, "r") as f:
        expected_html = f.read()

    expected_html = expected_html.replace("{{PEAK_TIME}}", str(peak_time))
    expected_html = expected_html.replace("{{ERROR_COUNT}}", str(max_count))
    expected_html = expected_html.replace("{{SAMPLED_IPS}}", ", ".join(sampled_ips))

    try:
        response = requests.get("http://127.0.0.1:8080/latest_incident", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert response.text == expected_html, f"Response HTML does not match expected.\nExpected:\n{expected_html}\nActual:\n{response.text}"