# test_final_state.py

import os
import base64
import requests
import pytest

def get_expected_data():
    raw_file = '/home/user/raw_sensor_logs.txt'
    if not os.path.exists(raw_file):
        return [], 0

    with open(raw_file, 'r') as f:
        lines = f.read().splitlines()

    valid_rows = []
    for line in lines:
        if not line.strip():
            continue
        try:
            b = base64.b64decode(line)
            dec = bytes([x ^ 0x42 for x in b]).decode('utf-8')
        except Exception:
            continue

        parts = dec.strip().split(',')
        if len(parts) != 3:
            continue

        ts, sid, val = parts

        if val == "ERROR":
            continue
        try:
            if float(val) < 0:
                continue
        except ValueError:
            pass

        sid = sid.upper()
        valid_rows.append(f"{ts},{sid},{val}")

    unique_rows = list(set(valid_rows))
    # Standard linux sort behavior (lexicographical)
    unique_rows.sort()

    sensors = set(row.split(',')[1] for row in unique_rows)

    return unique_rows, len(sensors)

def test_server_cleaned_data():
    expected_rows, _ = get_expected_data()
    expected_csv = "\n".join(expected_rows)
    if expected_csv:
        expected_csv += "\n"

    try:
        response = requests.get("http://127.0.0.1:9090/cleaned_data.csv", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or fetch /cleaned_data.csv: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    actual_text = response.text.strip()
    expected_text = expected_csv.strip()

    assert actual_text == expected_text, "The served cleaned_data.csv content does not match the expected filtered, normalized, and sorted data."

def test_server_report_html():
    expected_rows, sensor_count = get_expected_data()
    count = len(expected_rows)

    expected_html = f"""<html>
<body>
<h1>Sensor Data Report</h1>
<p>Total Cleaned Records: {count}</p>
<p>Unique Sensors: {sensor_count}</p>
</body>
</html>"""

    try:
        response = requests.get("http://127.0.0.1:9090/report.html", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or fetch /report.html: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    actual_html = response.text.strip().replace('\r\n', '\n')
    expected_html_clean = expected_html.strip().replace('\r\n', '\n')

    assert actual_html == expected_html_clean, "The served report.html content does not match the expected HTML template and counts."